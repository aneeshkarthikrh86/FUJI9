from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime

def Launch_browser(page, url):
    page.goto(url, wait_until = "load", timeout = 60000)
    return page.title()
   
def Screenshots(page, Gamenamet):
    folder = "Screenshots"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    filename = f"{Gamenamet}_{timestamp}.png".replace(" ", "_")
    path = os.path.join(folder, filename)
    page.screenshot(path=path, full_page=True)

def close_popup(page):
    Cancelpopup = page.locator("//div[contains(@class, 'min-h-[var(--window-height)]')]/div/button/img")
    try:
        Cancelpopup.wait_for(state = "visible", timeout = 7000)
        Cancelpopup.click()
        print("Ads popup closed successfully")
    except:
        print("Adds popup not found.")
    
def Login(page, username, password):
    page.locator("//div[@class='flex relative items-center']/div/div/button[text()='Login']").click()
    page.locator("//div[@class='rounded-[5px] modal_login_form_box py-4 px-6 border']//input[@placeholder = 'Enter Your Username']").fill(username)
    page.locator("//input[@placeholder = 'Password']").fill(password)
    page.locator("//div[@class='relative flex justify-center']//button[text() = 'Login']").click()
    
def SlotHome(page):
    page.locator("//a[text()=' Slot']").click()
    page.locator("//a[text()=' Home']").hover()
    time.sleep(1)
    
def Provider(page):
    # page.locator("//div[@class='tab_btn_bg relative overflow-hidden']/img[contains(@alt, 'PP')]").click()
    # ProviderName = page.locator("//div[text() = 'PP']").inner_text()
    # print(f"Provider Name: {ProviderName}")
    Providers_list_xpath = "//div[@class='mt-5 flex items-center slot_btn_container w-full overflow-auto light-scrollbar-h pb-[10px]']//button"
    Providers_Name_xpath = "//div[@class='mt-5 flex items-center slot_btn_container w-full overflow-auto light-scrollbar-h pb-[10px]']//button//div[@class='tab_btn_text text-center text-xs mt-2 uppercase w-[50px] truncate']"
    
    Providers = page.locator(Providers_list_xpath)
    ProviderNames = page.locator(Providers_Name_xpath)
    Total_Providers = Providers.count()
    print(f"Total Providers: {Total_Providers}")
    for prov in range(2, Total_Providers):
        provider = Providers.nth(prov)
        providername = ProviderNames.nth(prov).inner_text()
        provider.scroll_into_view_if_needed()
        provider.click()
        print(f"Provider Name: {providername}")
        Pagination(page, providername)
    
def GameTesting(page, providername, p):
    GamesNames = "//div[@class='game_btn_content_text']"
    Games = "//div[@class='game_btn_content']//button[text()='Play Now']"
    
    Game = page.locator(Games)
    Gamename = page.locator(GamesNames)
    
    Total_Games = Game.count()
    print(f"Total Games: {Total_Games}")
    # GamesToBeTested = min(3, Total_Games)
    for g in range(Total_Games):
        try:
            Gamenamet = Gamename.nth(g).inner_text()
            gameplay = Game.nth(g)
            time.sleep(2)
            gameplay.scroll_into_view_if_needed()
            time.sleep(2)
            gameplay.hover()
            time.sleep(2)
            gameplay.evaluate("el => el.click()")
            # Game opened in same page
            toast_selector = page.locator("//div[@class='toast-message text-sm' and contains(text(),'Something went wrong')]")
            toast_visible = False
            for _ in range(10):
                try:
                    if toast_selector.is_visible():
                        toast_visible = True
                        break
                except:
                    pass
                time.sleep(2)
                
            if toast_visible:
                print(f"Failed: {Gamenamet}")
                try:
                    page.locator("//button[text()='Back To Home']").click()
                except:
                    page.go_back()
            else:
                # Screenshots(page, Gamenamet)

                error_found = False

                for frame in page.frames:
                    try:
                        # Explicitly check if the element is visible
                        if frame.locator("text=Sorry, the game is not available for your jurisdiction.").is_visible():
                            Screenshots(page, Gamenamet)
                            print(f"Success: {Gamenamet} with Jurisdiction Blocked Messg.")
                            error_found = True
                            break
                    except:
                        continue

                if not error_found:
                    print(f"Success: {Gamenamet}")
                    # Cancel_btn = page.locator("//button/*[@class='w-5 h-5 game_header_close_btn']")
                try:
                    page.locator("//button/*[@class='w-5 h-5 game_header_close_btn']").click()
                except:
                    page.go_back()
                        
        except Exception as e:
            
            try:
                Gamenamet = Gamename.nth(g).inner_text()
                gameplay = Game.nth(g)
                page.wait_for_timeout(2000)
                Gamenamet.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
                Gamenamet.hover()
                page.wait_for_timeout(2000)
                gameplay.evaluate("el => el.click()")
                page.wait_for_timeout(2000)
            except:
                Screenshots (page, Gamenamet)
                print(f"failed {Gamenamet} {providername} as {e}")
                continue
            
            
        if p != 1:
            try:
                btn1 = page.locator("//div[@class='p-holder admin-pagination']/button[normalize-space(text())='1']")
                time.sleep(2)
                btn1.scroll_into_view_if_needed()
                time.sleep(2)
                btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{p}']")
                while not btn.is_visible():
                    visible_btns = page.locator("//div[@class='p-holder admin-pagination']/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]")
                    visible = visible_btns.nth(visible_btns.count()-2)
                    visible.click()
                    time.sleep(1)
                btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{p}']")
                btn.click()
                time.sleep(1)
            except Exception as e:
                Screenshots (page, Gamenamet)
                print(f"failed {Gamenamet} {providername} after game rather than 1st page {e}")

            
def Pagination(page, providername):
    pagination_buttons = "//div[@class='p-holder admin-pagination']/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]"
    Pagination_Button = page.locator(pagination_buttons)
    Total_Pages = int(Pagination_Button.last.inner_text())
    print(f"Total Pages: {Total_Pages} in {providername}")
    for p in range(1, Total_Pages+1):
        if p >1:
            btn1 = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='1']")
            time.sleep(1)
            btn1.scroll_into_view_if_needed()
            time.sleep(1)
            btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{p}']")
            while not btn.is_visible():
                visible_btns = page.locator(pagination_buttons)
                last_visible = visible_btns.nth(visible_btns.count()-2)
                print(f"Page {last_visible.inner_text()} for reveal")
                last_visible.click()
                time.sleep(1)
            btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{p}']")
            btn.click()
            time.sleep(1)
        GameTesting(page, providername, p)
    
    
with sync_playwright() as p:
    browser = p.chromium.launch(headless = False, args = ["--Start-maximized"])
    context = browser.new_context(no_viewport = True, record_video_dir="Videos/")
    page = context.new_page()
    title = Launch_browser(page, "https://www.fuji9bd.com/en-ph/")
    page.screenshot(path="videos/screenshot.png")
    print(title)
    close_popup(page)
    Login(page, "testphp", "qweqwe11")
    close_popup(page)
    SlotHome(page)
    Provider(page)
    browser.close()