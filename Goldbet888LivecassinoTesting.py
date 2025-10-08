from playwright.sync_api import sync_playwright
import os
import time
from datetime import datetime

def screenshot(page, gamename):
    folder = "Screenshot"
    if not os.path.exists(folder):
        os.makedirs("folder")
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    filename = f"{gamename}_{timestamp}.png.".replace(" ", "_")
    path = os.path.join(folder, filename)
    page.screenshot(path=path, fullpage=True)
    
def Launch_Url(page, url):
    page.goto(url)
    return page.title()
    
def close_popup(page):
   AdPopClose = page.locator("//div[contains(@class, 'min-h-[var(--window-height)]')]/div/button/img")
   try:
       AdPopClose.wait_for(state = "visible", timeout = 10000)
       AdPopClose.click()
       print("Adpopup is closed")
   except:
       print("Adpopup not present")
       
def missionpopupcancel(page):
    missioncancel = page.locator("//button[@class='mission_daily_close_btn']/img")
    try:
        missioncancel.wait_for(state = "visible", timeout = 10000)
        missioncancel.click()
        print("missionpopup is closed")
    except:
        print("missionpopup not present")
    
def Login(page, username, password):
    page.wait_for_timeout(2000)
    page.locator("//button[@class='topbar_btn_1 hidden md:block' and text()='Login']").click()
    page.locator("//div[@class='rounded-[5px] modal_login_form_box py-4 px-6 border']//input[@placeholder = 'Enter Your Username']").fill(username)
    page.locator("//input[@placeholder = 'Password']").fill(password)
    page.locator("//div[@class='relative flex justify-center']//button[text() = 'Login']").click()
    
def slothome(page):
    Slot = page.locator("//a[text()=' Slot']")
    Slot.wait_for(state = "visible", timeout = 10000)
    Slot.click()
    page.locator("//a[text()=' Home']").hover()
    page.wait_for_timeout(2000)
    
def Providers(page):
    Providers_list_xpath = "//div[@class='mt-5 flex items-center slot_btn_container w-full overflow-auto light-scrollbar-h pb-[10px]']//button"
    Providers_Name_xpath = "//div[@class='mt-5 flex items-center slot_btn_container w-full overflow-auto light-scrollbar-h pb-[10px]']//button//div[@class='tab_btn_text text-center text-xs mt-2 uppercase w-[50px] truncate']"
    
    Providers = page.locator(Providers_list_xpath)
    ProviderNames = page.locator(Providers_Name_xpath)
    Total_Provider = Providers.count()
    print(f"Total Providers: {Total_Provider}")
    
    for i in range(Total_Provider):
        ProviderName = ProviderNames.nth(i).inner_text()
        Provider = Providers.nth(i)
        Provider.click()
        page.wait_for_timeout(2000)
        print(f"Provider Name: {ProviderName}")
        page.wait_for_timeout(2000)
        
        pagination(page, ProviderName)
        
def pagination(page, ProviderName):
    PaginationButtons = "//div[@class='p-holder admin-pagination']/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]"
    PaginationButton = page.locator(PaginationButtons)
    LastPage = int(PaginationButton.last.inner_text())
    print(f"Total Page: {LastPage}") 
    
    for pa in range(1, LastPage+1):
        if pa >1:
            btn1 = page.locator("//div[@class='p-holder admin-pagination']/button[normalize-space(text())='1']")
            page.wait_for_timeout(2000)
            btn1.scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{pa}']")
            while not btn.is_visible():
                visible_buttons = PaginationButton = page.locator(PaginationButtons)
                visiblebtn = visible_buttons.nth(visible_buttons.count()-2)
                page.wait_for_timeout(2000)
                visiblebtn.click()
                page.wait_for_timeout(2000)
            btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{pa}']")
            btn.click()                
            page.wait_for_timeout(2000)
            GameTesting(page, ProviderName, pa)
            

def GameTesting(page, ProviderName, pa):
    GamesNames = "//div[@class='game_btn_content_text']"
    Games = "//div[@class='game_btn_content']//button[text()='Play Now']"
    
    GameNames = page.locator(GamesNames)
    GamePlays = page.locator(Games)
    
    TotalGames = GameNames.count()
    print(f"Total Games: {TotalGames}")
    
    for ga in range(TotalGames):
        try:
            GameName = GameNames.nth(ga).inner_text()
            GamePlay = GamePlays.nth(ga)
            GameName.scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            GameName.hover()
            page.wait_for_timeout(2000)
            GamePlay.evaluate("el => el.click()")
            
            toast_selector = page.locator("//div[@class='toast-message text-sm' and contains(text(),'Something went wrong')]")
            Toast_Exist = False
            
            for _ in range(7.5):
                try:
                    if toast_selector.is_visible():
                        Toast_Exist = True
                        break
                except:
                    pass
                page.wait_for_timeout(2000)
                
            if Toast_Exist:
                print(f"Failed: {GameName}")
                try:
                    page.locator("//button[text()='Back To Home']").click()
                except:
                    page.go_back()
                    
            else:
                
                
                error_found = False
                
                for frame in page.frames:
                    try:
                        if frame.locator("text=Sorry, the game is not available for your jurisdiction.").is_visible():
                            screenshot(page, GameName)
                            print(f"Success: {GameName} * ")
                            print(f"❌ Jurisdiction Blocked: {GameName}")
                            error_found = True
                            break
                    except:
                        continue 
                if not error_found:
                    print(f"Success: {GameName}")
                    try:
                        page.locator("//button/*[@class='w-5 h-5 game_header_close_btn']").click()
                    except:
                        page.go_back()
        except:
            try:
                GameName = GameNames.nth(ga).inner_text()
                gameplay = GamePlays.nth(ga)
                page.wait_for_timeout(2000)
                GameName.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
                GameName.hover()
                page.wait_for_timeout(2000)
                gameplay.evaluate("el => el.click()")
                page.wait_for_timeout(2000)
            except Exception as e:
                screenshot(page, GameName)
                print(f"failed {GameName} {ProviderName} as {e}")
                continue
            
        if pa > 1:
            try:
                btn1 = page.locator("//div[@class='p-holder admin-pagination']/button[normalize-space(text())='1']")
                page.wait_for_timeout(2000)
                btn1.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
                btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{pa}']")
                while not btn.is_visible():
                    PaginationButtons = "//div[@class='p-holder admin-pagination']/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]"
                    visible_buttons = page.location(PaginationButtons)
                    visibleBtn = visible_buttons.nth(visible_buttons.count()-2)
                    visibleBtn.click()
                page.wait_for_timeout(2000)
                btn = page.locator(f"//div[@class='p-holder admin-pagination']/button[normalize-space(text())='{pa}']")
                btn.click()
                page.wait_for_timeout(2000) 
            except Exception as e:
                screenshot(page, GameName)
                print(f"Failed Due to exception: {GameName} {ProviderName}")
                continue
            
            
                
            
        
        
        
        

    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args = ["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    get_text = Launch_Url(page, "https://www.gb888sg2.com/en-sg/")
    print(get_text)
    close_popup(page)
    missionpopupcancel(page)
    Login(page, "testacc", "qweqwe11")
    close_popup(page)
    missionpopupcancel(page)
    slothome(page)
    Providers(page)
    browser.close()
    
    
    
    