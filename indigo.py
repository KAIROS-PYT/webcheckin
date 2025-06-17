#!/usr/bin/env python3
"""
IndiGo Web Check-in Form Filler - Enhanced Diagnostic Version
Debug why fields aren't being filled
"""

from playwright.sync_api import sync_playwright
import time

def fill_indigo_form():
    # Your details
    PNR = "Y2FZMW"
    LAST_NAME = "Seshadri"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        page = browser.new_page()
        
        # Set viewport and user agent to mimic real browser
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        print("Opening IndiGo web check-in page...")
        
        try:
            page.goto("https://www.goindigo.in/web-check-in.html", timeout=30000)
            print("✅ Page navigation successful")
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return
        
        print("Waiting for page to fully load...")
        time.sleep(5)
        
        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")
        
        # Wait for any dynamic content to load
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
            print("✅ Network idle state reached")
        except:
            print("⚠️ Network didn't reach idle state, continuing...")
        
        # Check for iframes (form might be in an iframe)
        print("\n=== Checking for iframes ===")
        frames = page.frames
        print(f"Total frames found: {len(frames)}")
        
        main_frame = page
        form_frame = None
        
        for i, frame in enumerate(frames):
            try:
                frame_url = frame.url
                print(f"Frame {i}: {frame_url}")
                
                # Check if this frame contains form elements
                inputs_in_frame = frame.query_selector_all("input")
                if len(inputs_in_frame) > 0:
                    print(f"  Frame {i} has {len(inputs_in_frame)} input fields!")
                    form_frame = frame
            except Exception as e:
                print(f"  Frame {i}: Error - {e}")
        
        # Use the frame that contains form elements, or main page
        working_frame = form_frame if form_frame else main_frame
        
        if form_frame:
            print(f"✅ Using frame with form elements")
        else:
            print("Using main page")
        
        # Comprehensive field search
        print(f"\n{'='*60}")
        print("COMPREHENSIVE FIELD SEARCH")
        print(f"{'='*60}")
        
        # Get ALL input fields
        all_inputs = working_frame.query_selector_all("input")
        print(f"Found {len(all_inputs)} total input fields")
        
        pnr_candidates = []
        name_candidates = []
        
        for i, inp in enumerate(all_inputs):
            try:
                name_attr = inp.get_attribute("name") or ""
                id_attr = inp.get_attribute("id") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                type_attr = inp.get_attribute("type") or "text"
                class_attr = inp.get_attribute("class") or ""
                visible = inp.is_visible()
                enabled = inp.is_enabled()
                
                print(f"\nInput {i}:")
                print(f"  name: '{name_attr}'")
                print(f"  id: '{id_attr}'")
                print(f"  type: '{type_attr}'")
                print(f"  placeholder: '{placeholder}'")
                print(f"  class: '{class_attr}'")
                print(f"  visible: {visible}")
                print(f"  enabled: {enabled}")
                
                # Check if this could be PNR field
                pnr_keywords = ['pnr', 'booking', 'reference', 'confirmation']
                if any(keyword in (name_attr + id_attr + placeholder + class_attr).lower() 
                       for keyword in pnr_keywords):
                    if visible and enabled:
                        pnr_candidates.append((i, inp, f"name='{name_attr}' id='{id_attr}' placeholder='{placeholder}'"))
                        print(f"  ⭐ POTENTIAL PNR FIELD")
                
                # Check if this could be Name field
                name_keywords = ['name', 'email', 'passenger', 'surname', 'lastname']
                if any(keyword in (name_attr + id_attr + placeholder + class_attr).lower() 
                       for keyword in name_keywords):
                    if visible and enabled:
                        name_candidates.append((i, inp, f"name='{name_attr}' id='{id_attr}' placeholder='{placeholder}'"))
                        print(f"  ⭐ POTENTIAL NAME FIELD")
                        
            except Exception as e:
                print(f"Input {i}: Error reading attributes - {e}")
        
        print(f"\n{'='*60}")
        print("FIELD CANDIDATES")
        print(f"{'='*60}")
        print(f"PNR candidates: {len(pnr_candidates)}")
        for i, (idx, elem, desc) in enumerate(pnr_candidates):
            print(f"  {i+1}. Input {idx}: {desc}")
        
        print(f"\nName candidates: {len(name_candidates)}")
        for i, (idx, elem, desc) in enumerate(name_candidates):
            print(f"  {i+1}. Input {idx}: {desc}")
        
        # Try to fill PNR field
        print(f"\n{'='*60}")
        print("ATTEMPTING TO FILL PNR")
        print(f"{'='*60}")
        
        pnr_filled = False
        for i, (idx, pnr_field, desc) in enumerate(pnr_candidates):
            try:
                print(f"Trying PNR candidate {i+1}: {desc}")
                
                # Multiple approaches to fill the field
                print("  Approach 1: Direct fill")
                pnr_field.fill(PNR)
                current_value = pnr_field.input_value()
                print(f"  Value after fill: '{current_value}'")
                
                if current_value != PNR:
                    print("  Approach 2: Click then fill")
                    pnr_field.click()
                    time.sleep(0.5)
                    pnr_field.fill(PNR)
                    current_value = pnr_field.input_value()
                    print(f"  Value after click+fill: '{current_value}'")
                
                if current_value != PNR:
                    print("  Approach 3: Clear then type")
                    pnr_field.click()
                    time.sleep(0.5)
                    pnr_field.press("Control+a")
                    pnr_field.type(PNR)
                    current_value = pnr_field.input_value()
                    print(f"  Value after clear+type: '{current_value}'")
                
                if current_value == PNR:
                    print(f"  ✅ PNR successfully filled: {PNR}")
                    pnr_filled = True
                    break
                else:
                    print(f"  ❌ PNR fill failed")
                    
            except Exception as e:
                print(f"  ❌ Error filling PNR candidate {i+1}: {e}")
        
        # Try to fill Name field
        print(f"\n{'='*60}")
        print("ATTEMPTING TO FILL NAME")
        print(f"{'='*60}")
        
        name_filled = False
        for i, (idx, name_field, desc) in enumerate(name_candidates):
            try:
                print(f"Trying Name candidate {i+1}: {desc}")
                
                # Multiple approaches to fill the field
                print("  Approach 1: Direct fill")
                name_field.fill(LAST_NAME)
                current_value = name_field.input_value()
                print(f"  Value after fill: '{current_value}'")
                
                if current_value != LAST_NAME:
                    print("  Approach 2: Click then fill")
                    name_field.click()
                    time.sleep(0.5)
                    name_field.fill(LAST_NAME)
                    current_value = name_field.input_value()
                    print(f"  Value after click+fill: '{current_value}'")
                
                if current_value != LAST_NAME:
                    print("  Approach 3: Clear then type")
                    name_field.click()
                    time.sleep(0.5)
                    name_field.press("Control+a")
                    name_field.type(LAST_NAME)
                    current_value = name_field.input_value()
                    print(f"  Value after clear+type: '{current_value}'")
                
                if current_value == LAST_NAME:
                    print(f"  ✅ Name successfully filled: {LAST_NAME}")
                    name_filled = True
                    break
                else:
                    print(f"  ❌ Name fill failed")
                    
            except Exception as e:
                print(f"  ❌ Error filling Name candidate {i+1}: {e}")
        
        # Check if fields were filled successfully
        print(f"\n{'='*60}")
        print("FILL RESULTS")
        print(f"{'='*60}")
        print(f"PNR filled: {pnr_filled}")
        print(f"Name filled: {name_filled}")
        
        if pnr_filled and name_filled:
            print("\n✅ Both fields filled successfully!")
            
            # Wait for button to be enabled
            print("Waiting for submit button to be enabled...")
            time.sleep(3)
            
            # Look for submit button
            print("\n=== Looking for Submit Button ===")
            button_selectors = [
                "button[title='Web Check-In with IndiGo']",
                "button:has-text('Web check-in')",
                "button[type='submit']",
                "input[type='submit']",
                ".skyplus-button--filled"
            ]
            
            button_found = False
            for selector in button_selectors:
                try:
                    buttons = working_frame.query_selector_all(selector)
                    for j, button in enumerate(buttons):
                        text = button.inner_text().strip()
                        visible = button.is_visible()
                        enabled = button.is_enabled()
                        disabled = button.get_attribute("disabled")
                        
                        print(f"Button with selector '{selector}' #{j}:")
                        print(f"  Text: '{text}'")
                        print(f"  Visible: {visible}")
                        print(f"  Enabled: {enabled}")
                        print(f"  Disabled attr: {disabled}")
                        
                        if visible and enabled and not disabled:
                            print(f"  Clicking button...")
                            button.click()
                            print(f"  ✅ Button clicked!")
                            button_found = True
                            break
                    
                    if button_found:
                        break
                        
                except Exception as e:
                    print(f"Error with selector '{selector}': {e}")
            
            if not button_found:
                print("❌ Could not find or click submit button")
        
        else:
            print("❌ Fields not filled properly, cannot proceed to button click")
        
        print(f"\n{'='*60}")
        print("Keeping browser open for 60 seconds for manual inspection...")
        time.sleep(60)
        browser.close()

if __name__ == "__main__":
    fill_indigo_form()