"""
Scraper for Merolagani.com - Real-time NEPSE stock prices using Selenium
Handles JavaScript-rendered content from Merolagani website
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import Dict, List, Optional, Any
import logging
import time
import json

logger = logging.getLogger(__name__)

class MerolaganiScraper:
    """Scrapes real-time NEPSE stock prices from Merolagani.com using Selenium"""
    
    BASE_URL = "https://www.merolagani.com"
    STOCK_QUOTE_PATH = "/StockQuote"
    DRIVER_TIMEOUT = 20
    
    @staticmethod
    def _get_driver():
        """Create and configure Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Try to use webdriver-manager if available
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                driver = webdriver.Chrome(
                    service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                    options=chrome_options
                )
            except ImportError:
                # Fallback: chromedriver should be in PATH
                driver = webdriver.Chrome(options=chrome_options)
            
            logger.info("✅ WebDriver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"❌ Failed to initialize Chrome WebDriver: {e}")
            logger.info("💡 Install ChromeDriver: pip install webdriver-manager")
            return None
    
    @classmethod
    def _extract_price_from_text(cls, text: str) -> Optional[float]:
        """Extract numeric price from text"""
        try:
            # Remove non-numeric characters except decimal point
            cleaned = text.replace(',', '').replace('Rs.', '').replace('Rs', '').strip()
            if cleaned:
                return float(cleaned)
        except:
            pass
        return None
    
    @classmethod
    def get_all_stock_prices(cls) -> Dict[str, Dict[str, Any]]:
        """
        Fetch all stock prices from Merolagani market page
        Returns dictionary with symbol as key and price data as value
        """
        driver = None
        try:
            driver = cls._get_driver()
            if not driver:
                logger.warning("⚠️ WebDriver not available, returning empty dict")
                return {}
            
            market_url = f"{cls.BASE_URL}{cls.STOCK_QUOTE_PATH}"
            logger.info(f"🔍 Loading Merolagani market page: {market_url}")
            driver.get(market_url)
            
            # Wait for page content to load - try multiple selectors
            wait = WebDriverWait(driver, cls.DRIVER_TIMEOUT)
            stocks = {}
            
            # Strategy 1: Wait for any visible content
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(3)  # Give JavaScript time to render
                
                # Look for various container elements that might have price data
                page_source = driver.page_source
                logger.debug(f"Page source length: {len(page_source)}")
                
                # Try to find price data in JavaScript arrays/objects
                # Merolagani often renders data via JavaScript
                if 'ltp' in page_source.lower() or 'price' in page_source.lower():
                    logger.info("✅ Found price-related content in page")
            except Exception as e:
                logger.warning(f"Timeout waiting for page load: {e}")
            
            # Strategy 2: Look for data in different table structures
            try:
                # Try multiple XPath patterns
                xpaths = [
                    "//table//tr[td]",  # Standard table rows with data cells
                    "//div[contains(@class, 'table')]//tr",  # Divs styled as tables
                    "//tbody//tr",  # Explicit tbody
                    "//tr[@data-symbol]",  # Rows with data attributes
                ]
                
                for xpath in xpaths:
                    try:
                        rows = driver.find_elements(By.XPATH, xpath)
                        if rows:
                            logger.info(f"📊 Found {len(rows)} rows using XPath: {xpath}")
                            
                            for idx, row in enumerate(rows):
                                try:
                                    cells = row.find_elements(By.TAG_NAME, "td")
                                    if len(cells) >= 2:
                                        symbol_text = cells[0].text.strip().upper()
                                        if not symbol_text or len(symbol_text) > 10 or not symbol_text.isalpha():
                                            continue
                                        
                                        try:
                                            price_text = cells[1].text.strip()
                                            price = cls._extract_price_from_text(price_text)
                                            
                                            if price and price > 0:
                                                stocks[symbol_text] = {
                                                    'symbol': symbol_text,
                                                    'current_price': price,
                                                    'ltp': price
                                                }
                                                logger.debug(f"✓ {symbol_text}: Rs. {price}")
                                        except (ValueError, IndexError):
                                            continue
                                except Exception as cell_error:
                                    logger.debug(f"Cell error: {cell_error}")
                                    continue
                            
                            if stocks:
                                logger.info(f"✅ Successfully scraped {len(stocks)} stocks")
                                return stocks
                    except Exception as xpath_error:
                        logger.debug(f"XPath {xpath} failed: {xpath_error}")
                        continue
                
            except Exception as e:
                logger.error(f"Error finding rows: {e}")
            
            # Strategy 3: Look for any data in common element IDs/classes
            try:
                logger.info("Trying alternative selectors...")
                elements = driver.find_elements(By.XPATH, "//*[@class or @id]")
                
                for elem in elements[:100]:  # Check first 100 elements
                    try:
                        text = elem.text
                        if any(stock in text.upper() for stock in ['UPPER', 'AAAAA', 'ADBL']):
                            logger.debug(f"Found stock reference in: {elem.get_attribute('class')} / {elem.get_attribute('id')}")
                    except:
                        pass
            except:
                pass
            
            if not stocks:
                logger.warning("❌ Could not extract any stock prices from page")
                logger.info("💡 Note: Merolagani structure may have changed. Check website manually.")
            
            return stocks
            
        except Exception as e:
            logger.error(f"❌ Error scraping Merolagani: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {}
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    @classmethod
    def get_stock_price(cls, symbol: str) -> Optional[float]:
        """
        Fetch price for a specific stock from Merolagani
        """
        driver = None
        try:
            driver = cls._get_driver()
            if not driver:
                return None
            
            url = f"{cls.BASE_URL}{cls.STOCK_QUOTE_PATH}/{symbol.upper()}"
            logger.info(f"🔍 Fetching price for {symbol} from {url}")
            driver.get(url)
            
            # Wait for page to load
            wait = WebDriverWait(driver, cls.DRIVER_TIMEOUT)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Give JavaScript time to render
            
            # Try multiple strategies to find price
            price = None
            
            # Strategy 1: Look for common price element patterns
            selectors = [
                ("ltp", By.CLASS_NAME),
                ("price", By.CLASS_NAME),
                ("current-price", By.CLASS_NAME),
                ("//span[contains(@class, 'ltp')]", By.XPATH),
                ("//div[contains(@class, 'price')]//span", By.XPATH),
            ]
            
            for selector, by_type in selectors:
                try:
                    elements = driver.find_elements(by_type, selector)
                    if elements:
                        for elem in elements:
                            text = elem.text.strip()
                            if text:
                                extracted = cls._extract_price_from_text(text)
                                if extracted and extracted > 0:
                                    price = extracted
                                    logger.info(f"✅ Got price for {symbol}: Rs. {price}")
                                    return price
                except:
                    pass
            
            # Strategy 2: Search entire page for the price
            page_text = driver.page_source
            if symbol.upper() in page_text:
                logger.debug(f"Symbol found in page source")
                # Try to find price near the symbol
                try:
                    all_text = driver.find_element(By.TAG_NAME, "body").text
                    lines = all_text.split('\n')
                    for i, line in enumerate(lines):
                        if symbol.upper() in line and i + 1 < len(lines):
                            next_line = lines[i + 1]
                            price = cls._extract_price_from_text(next_line)
                            if price and price > 0:
                                logger.info(f"✅ Found price for {symbol}: Rs. {price}")
                                return price
                except:
                    pass
            
            logger.warning(f"⚠️ Could not find price for {symbol}")
            return price
            
        except Exception as e:
            logger.error(f"❌ Error fetching price for {symbol}: {e}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    @classmethod
    def search_stocks(cls, query: str) -> List[Dict[str, Any]]:
        """
        Search for stocks by symbol
        """
        try:
            all_stocks = cls.get_all_stock_prices()
            query_upper = query.upper()
            
            results = [
                {'symbol': k, **v} 
                for k, v in all_stocks.items()
                if query_upper in k
            ]
            
            logger.info(f"🔍 Search for '{query}' found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching stocks: {e}")
            return []
