# -*- coding: utf-8 -*-
from PIL import ImageTk,Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageColor
try:
    from bidi import get_display as bidi_get_display
except:
    from bidi.algorithm import get_display as bidi_get_display
import os
import sys
import math
import tkinter as tk
from tkinter import font
from tkinter import filedialog, simpledialog, messagebox, ttk
import shutil
import re
import traceback
import platform
import threading
import queue
import time
import json
import subprocess
import shutil
import numpy as np

deviceScreenWidth, deviceScreenHeight = 640, 480

if getattr(sys, 'frozen', False):
    # The application is running as a bundle
    internal_files_dir = sys._MEIPASS
    script_dir = os.path.dirname(sys.executable)
else:
    # The application is running in a normal Python environment
    internal_files_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(os.path.abspath(__file__))

#HI
# Default values for parameters
class Config:
    def __init__(self, config_file=os.path.join(script_dir,'MinUIThemeGeneratorConfig.json')):
        self.config_file = config_file
        self.scrollBarWidthVar = 10
        self.textPaddingVar = 25
        self.bubblePaddingVar = 20
        self.itemsPerScreenVar = 9
        self.footerHeightVar = 55
        self.override_font_size_var = False
        self.legacy_generation_var = False
        self.customFontSizeVar = ""
        self.bgHexVar = "000000"
        self.selectedFontHexVar = "000000"
        self.deselectedFontHexVar = "ffffff"
        self.bubbleHexVar = "ffffff"
        self.iconHexVar = "ffffff"
        self.remove_brackets_var = False
        self.remove_square_brackets_var = False
        self.replace_hyphen_var = False
        self.also_games_var = False
        self.move_the_var = False
        self.include_overlay_var = False
        self.alternate_menu_names_var = False
        self.remove_right_menu_guides_var = False
        self.remove_left_menu_guides_var = False
        self.overlay_box_art_var = False
        self.boxArtPaddingVar = 0
        self.folderBoxArtPaddingVar = 0
        self.box_art_directory_path = ""
        self.maxGamesBubbleLengthVar = deviceScreenWidth
        self.maxFoldersBubbleLengthVar = deviceScreenWidth
        self.roms_directory_path = ""
        self.application_directory_path = ""
        self.previewConsoleNameVar = "Nintendo Game Boy"
        self.show_hidden_files_var = False
        self.override_bubble_cut_var = False
        self.override_folder_box_art_padding_var = False
        self.page_by_page_var = False
        self.transparent_text_var = False
        self.version_var = "Select a version"
        self.global_alignment_var = "Left"
        self.selected_overlay_var = "muOS Default CRT Overlay"
        self.theme_alignment_var = "Global"
        self.main_menu_style_var = "Horizontal"
        self.content_alignment_var = "Global"
        self.am_theme_directory_path = ""
        self.theme_directory_path = ""
        self.catalogue_directory_path = ""
        self.name_json_path = ""
        self.background_image_path = ""
        self.bootlogo_image_path = ""
        self.rg28xxVar = False
        self.alt_font_path = ""
        self.alt_text_path = "AlternativeMenuNames.json"
        self.use_alt_font_var = False
        self.use_custom_bootlogo_var = False
        self.themeName = "MinUIfied - Default Theme"
        self.amThemeName = "MinUIfied - Default AM Theme"
        self.am_ignore_theme_var = False
        self.am_ignore_cd_var = False
        self.advanced_error_var = False
        self.show_file_counter_var = False
        self.show_console_name_var = False
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config_data = json.load(file)
                self.__dict__.update(config_data)
        else:
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

background_image = None

# Define constants
render_factor = 5


ConsoleAssociationsPath = os.path.join(script_dir,"ConsoleAssociations.json")
defaultConsoleAssociationsPath = os.path.join(internal_files_dir,"_ConsoleAssociations.json")

headerHeight = 40
footerHeight = 55
textMF = 0.7
additions_Blank = "Blank"
additions_PowerHelpBackOkay = "PowerHelpBackOkay"
additions_powerHelpOkay = "PowerHelpOkay"
additions_Preview = "Preview"


def change_logo_color(input_path, hex_color):
    # Load the image
    img = Image.open(input_path).convert("RGBA")
    
    # Convert hex_color to RGBA
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Create a new image with the same size and the specified color
    color_image = Image.new("RGBA", img.size, (r, g, b, 255))
    
    # Get the alpha channel from the original image
    alpha = img.split()[3]
    
    # Composite the color image with the alpha channel
    result_image = Image.composite(color_image, Image.new("RGBA", img.size, (0, 0, 0, 0)), alpha)
    
    return result_image

def generateMenuHelperGuides(muOSSystemName,selected_font_path,colour_hex,render_factor):
    image = Image.new("RGBA", (deviceScreenWidth*render_factor, deviceScreenHeight*render_factor), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    
    menu_helper_guide_height = (9/11)*footerHeight
        
    in_smaller_bubble_font_size = menu_helper_guide_height*(16/45)*render_factor
    inSmallerBubbleFont = ImageFont.truetype(selected_font_path, in_smaller_bubble_font_size)

    in_bubble_font_size = menu_helper_guide_height*(19/45)*render_factor
    inBubbleFont = ImageFont.truetype(selected_font_path, in_bubble_font_size)

    single_letter_font_size = menu_helper_guide_height*(23/45)*render_factor
    singleLetterFont = ImageFont.truetype(selected_font_path, single_letter_font_size)

    powerText = "POWER"
    sleepText = "SLEEP"
    menuText = "MENU"
    helpText = "HELP"
    backText = "BACK"
    okayText = "OKAY"
    confirmText = "CONFIRM"
    launchText = "LAUNCH"
    aText = "A"
    bText = "B"
    if alternate_menu_names_var.get():
        powerText = bidi_get_display(menuNameMap.get("power", "POWER"))
        sleepText = bidi_get_display(menuNameMap.get("sleep","SLEEP"))
        menuText = bidi_get_display(menuNameMap.get("menu","MENU"))
        helpText = bidi_get_display(menuNameMap.get("help","HELP"))
        backText = bidi_get_display(menuNameMap.get("back","BACK"))
        okayText = bidi_get_display(menuNameMap.get("okay","OKAY"))
        confirmText = bidi_get_display(menuNameMap.get("confirm","CONFIRM"))
        launchText = bidi_get_display(menuNameMap.get("launch","LAUNCH"))
    
    horizontal_small_padding = menu_helper_guide_height*(5/45)
    horizontal_padding = menu_helper_guide_height*(6.5/45)
    horizontal_large_padding = menu_helper_guide_height*(8.5/45)
    
    bottom_guide_middle_y = deviceScreenHeight-horizontal_small_padding-(menu_helper_guide_height/2)

    
    #guide_bubble_height = 80
    guide_small_bubble_height = menu_helper_guide_height-(horizontal_padding*2)

    isb_ascent, isb_descent = inSmallerBubbleFont.getmetrics()
    isb_text_height = isb_ascent + isb_descent
    in_smaller_bubble_text_y = bottom_guide_middle_y*render_factor - (isb_text_height / 2)

    ib_ascent, ib_descent = inBubbleFont.getmetrics()
    ib_text_height = ib_ascent + ib_descent
    in_bubble_text_y = bottom_guide_middle_y*render_factor - (ib_text_height / 2)

    sl_text_bbox = singleLetterFont.getbbox(aText+bText)
    sl_text_height = sl_text_bbox[3]-sl_text_bbox[1]
    single_letter_text_y = bottom_guide_middle_y*render_factor - (sl_text_height / 2)-sl_text_bbox[1]

    if not remove_left_menu_guides_var.get():
        powerTextBbox = inSmallerBubbleFont.getbbox(powerText)
        powerTextWidth = powerTextBbox[2] - powerTextBbox[0]
        sleepTextBbox = inBubbleFont.getbbox(sleepText)
        sleepTextWidth = sleepTextBbox[2] - sleepTextBbox[0]
        totalWidth = horizontal_padding+horizontal_large_padding+(powerTextWidth/render_factor)+horizontal_large_padding+horizontal_small_padding+(sleepTextWidth/render_factor)+horizontal_large_padding
        smallerBubbleWidth = horizontal_large_padding+(powerTextWidth/render_factor)+horizontal_large_padding
        draw.rounded_rectangle( ## Power Behind Bubble
                [(horizontal_small_padding*render_factor, (bottom_guide_middle_y-menu_helper_guide_height/2)*render_factor), ((totalWidth+horizontal_small_padding)*render_factor, (bottom_guide_middle_y+menu_helper_guide_height/2)*render_factor)],
                radius=(menu_helper_guide_height/2)*render_factor,
                #fill=f"#{percentage_color(primary_colour_hex,secondary_colour_hex,0.133)}"
                fill = hex_to_rgb(colour_hex, alpha = 0.133)
            )
        draw.rounded_rectangle( # Power infront Bubble
                [((horizontal_small_padding+horizontal_padding)*render_factor, (bottom_guide_middle_y-guide_small_bubble_height/2)*render_factor), ((horizontal_small_padding+horizontal_padding+smallerBubbleWidth)*render_factor, (bottom_guide_middle_y+guide_small_bubble_height/2)*render_factor)],
                radius=(guide_small_bubble_height/2)*render_factor,
                fill=hex_to_rgb(colour_hex, alpha = 1)
            )
        powerTextX = horizontal_small_padding+horizontal_padding+horizontal_large_padding
        sleepTextX = horizontal_small_padding+horizontal_padding+horizontal_large_padding+(powerTextWidth/render_factor)+horizontal_large_padding+horizontal_small_padding
        draw.text(( powerTextX*render_factor,in_smaller_bubble_text_y), powerText, font=inSmallerBubbleFont, fill=(*ImageColor.getrgb(f"#{colour_hex}"), int(255*0.593)))
        draw.text(( sleepTextX*render_factor,in_bubble_text_y), sleepText, font=inBubbleFont, fill=f"#{colour_hex}")
    if not remove_right_menu_guides_var.get():
        circleWidth = guide_small_bubble_height
        confirmTextBbox = inBubbleFont.getbbox(confirmText)
        confirmTextWidth = confirmTextBbox[2] - confirmTextBbox[0]
        backTextBbox = inBubbleFont.getbbox(backText)
        backTextWidth = backTextBbox[2] - backTextBbox[0]
        launchTextBbox = inBubbleFont.getbbox(launchText)
        launchTextWidth = launchTextBbox[2] - launchTextBbox[0]
        aTextBbox = singleLetterFont.getbbox(aText)
        aTextWidth = aTextBbox[2] - aTextBbox[0]
        bTextBbox = singleLetterFont.getbbox(bText)
        bTextWidth = bTextBbox[2] - bTextBbox[0]

        RHM_Len = 0
        if muOSSystemName == "muxdevice" or muOSSystemName == "muxlaunch": # Just A and Confirm ( One Circle and confirmText plus padding )
            RHM_Len = horizontal_padding+circleWidth+horizontal_small_padding+(confirmTextWidth/render_factor)+horizontal_large_padding
        elif muOSSystemName == "muxconfig" or muOSSystemName == "muxinfo": # B and Back, A and Confirm ( Two Circle and confirmText and backText plus padding )
            RHM_Len = horizontal_padding+circleWidth+horizontal_small_padding+(backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(confirmTextWidth/render_factor)+horizontal_large_padding
        elif muOSSystemName == "muxapp": # B and Back, A and Launch ( Two Circle and launchText and backText plus padding )
            RHM_Len = horizontal_padding+circleWidth+horizontal_small_padding+(backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(launchTextWidth/render_factor)+horizontal_large_padding

        draw.rounded_rectangle( ## Left hand behind bubble
                [((deviceScreenWidth-horizontal_small_padding-RHM_Len)*render_factor, (bottom_guide_middle_y-menu_helper_guide_height/2)*render_factor), ((deviceScreenWidth-horizontal_small_padding)*render_factor, (bottom_guide_middle_y+menu_helper_guide_height/2)*render_factor)],
                radius=(menu_helper_guide_height/2)*render_factor,
                fill=hex_to_rgb(colour_hex, alpha = 0.133)
            )
        if muOSSystemName != "muxapp": ## Draw Confirm
            aConfirmCircleCenterX = deviceScreenWidth-horizontal_small_padding-((circleWidth/2)+horizontal_small_padding+(confirmTextWidth/render_factor)+horizontal_large_padding)
            draw.ellipse(((aConfirmCircleCenterX-(circleWidth/2))*render_factor, (bottom_guide_middle_y-(circleWidth/2))*render_factor,(aConfirmCircleCenterX+(circleWidth/2))*render_factor, (bottom_guide_middle_y+(circleWidth/2))*render_factor),fill=f"#{colour_hex}") # A Bubble
            
            aConfirmTextX = aConfirmCircleCenterX - ((aTextWidth/2)/render_factor)
            confimTextX = deviceScreenWidth-horizontal_small_padding-((confirmTextWidth/render_factor)+horizontal_large_padding)
            draw.text(( aConfirmTextX*render_factor,single_letter_text_y), aText, font=singleLetterFont, fill=(*ImageColor.getrgb(f"#{colour_hex}"), int(255*0.593)))
            draw.text(( confimTextX*render_factor,in_bubble_text_y), confirmText, font=inBubbleFont, fill=f"#{colour_hex}")
            
            if muOSSystemName == "muxconfig" or muOSSystemName == "muxinfo": # Draw Back
                bBackCircleCenterX = deviceScreenWidth-horizontal_small_padding-((circleWidth/2)+horizontal_small_padding+(backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(confirmTextWidth/render_factor)+horizontal_large_padding)
                draw.ellipse(((bBackCircleCenterX-(circleWidth/2))*render_factor, (bottom_guide_middle_y-(circleWidth/2))*render_factor,(bBackCircleCenterX+(circleWidth/2))*render_factor, (bottom_guide_middle_y+(circleWidth/2))*render_factor),fill=f"#{colour_hex}") # B Bubble

                bBackTextX = bBackCircleCenterX - ((bTextWidth/2)/render_factor)
                backTextX = deviceScreenWidth-horizontal_small_padding-((backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(confirmTextWidth/render_factor)+horizontal_large_padding)
                draw.text(( bBackTextX*render_factor,single_letter_text_y), bText, font=singleLetterFont, fill=(*ImageColor.getrgb(f"#{colour_hex}"), int(255*0.593)))
                draw.text(( backTextX*render_factor,in_bubble_text_y), backText, font=inBubbleFont, fill=f"#{colour_hex}")

        else: # Draw Launch
            aLaunchCircleCenterX = deviceScreenWidth-horizontal_small_padding-((circleWidth/2)+horizontal_small_padding+(launchTextWidth/render_factor)+horizontal_large_padding)
            draw.ellipse(((aLaunchCircleCenterX-(circleWidth/2))*render_factor, (bottom_guide_middle_y-(circleWidth/2))*render_factor,(aLaunchCircleCenterX+(circleWidth/2))*render_factor, (bottom_guide_middle_y+(circleWidth/2))*render_factor),fill=f"#{colour_hex}") # A Bubble

            aLaunchTextX = aLaunchCircleCenterX - ((aTextWidth/2)/render_factor)
            launchTextX = deviceScreenWidth-horizontal_small_padding-((launchTextWidth/render_factor)+horizontal_large_padding)
            draw.text(( aLaunchTextX*render_factor,single_letter_text_y), aText, font=singleLetterFont, fill=(*ImageColor.getrgb(f"#{colour_hex}"), int(255*0.593)))
            draw.text(( launchTextX*render_factor,in_bubble_text_y), launchText, font=inBubbleFont, fill=f"#{colour_hex}")

            bBackCircleCenterX = deviceScreenWidth-horizontal_small_padding-((circleWidth/2)+horizontal_small_padding+(backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(launchTextWidth/render_factor)+horizontal_large_padding)
            draw.ellipse(((bBackCircleCenterX-(circleWidth/2))*render_factor, (bottom_guide_middle_y-(circleWidth/2))*render_factor,(bBackCircleCenterX+(circleWidth/2))*render_factor, (bottom_guide_middle_y+(circleWidth/2))*render_factor),fill=f"#{colour_hex}") # B Bubble

            bBackTextX = bBackCircleCenterX - ((bTextWidth/2)/render_factor)
            backTextX = deviceScreenWidth-horizontal_small_padding-((backTextWidth/render_factor)+horizontal_large_padding+circleWidth+horizontal_small_padding+(launchTextWidth/render_factor)+horizontal_large_padding)
            draw.text(( bBackTextX*render_factor,single_letter_text_y), bText, font=singleLetterFont, fill=(*ImageColor.getrgb(f"#{colour_hex}"), int(255*0.593)))
            draw.text(( backTextX*render_factor,in_bubble_text_y), backText, font=inBubbleFont, fill=f"#{colour_hex}")
    return image


def generatePilImageVertical(progress_bar,workingIndex, muOSSystemName,listItems,additions,textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor,scrollBarWidth = 0, showScrollBar=False,numScreens=0,screenIndex=0,fileCounter="",folderName = None,transparent=False):
    progress_bar['value'] +=1
    #print(f"progress_bar Max = {progress_bar['maximum']} | progress_bar Value = {progress_bar['value']} | {100*(int(progress_bar['value'])/int(progress_bar['maximum']))}%")
    bg_rgb = hex_to_rgb(bg_hex)
    if not transparent:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)

        if background_image != None:
            image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
    else:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), (0,0,0,0))

    draw = ImageDraw.Draw(image)   
    if transparent_text_var.get():
        transparent_text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw_transparent = ImageDraw.Draw(transparent_text_image)
        transparency = 0

    boxArtDrawn = False
    boxArtWidth = 0
    if len(listItems) == 0:
        return(image)
    if not use_alt_font_var.get():
        selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    else:
        if os.path.exists(alt_font_path.get()):
            selected_font_path = alt_font_path.get()
        else:
            selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")

    
    if additions != "Blank" and version_var.get() == "muOS 2405 BEANS" and not remove_right_menu_guides_var.get(): ## muOS Beans shit
        in_smaller_bubble_font_size = 16*render_factor
        inSmallerBubbleFont = ImageFont.truetype(selected_font_path, in_smaller_bubble_font_size)

        in_bubble_font_size = 19*render_factor 
        inBubbleFont = ImageFont.truetype(selected_font_path, in_bubble_font_size)

        single_letter_font_size = 23*render_factor
        singleLetterFont = ImageFont.truetype(selected_font_path, single_letter_font_size)
        RHM_Len = 340
        if additions == "PowerHelpOkay":
            RHM_Len = 240

        draw.rounded_rectangle(
                [(5*render_factor, 430*render_factor), (150*render_factor, 475*render_factor)],
                radius=22.5*render_factor,
                fill=f"#{percentage_color(bg_hex,bubble_hex,0.133)}"
            )
        draw.rounded_rectangle(
                [((deviceScreenWidth-5-RHM_Len)*render_factor, 430*render_factor), ((deviceScreenWidth-5)*render_factor, 475*render_factor)],
                radius=22.5*render_factor,
                fill=f"#{percentage_color(bg_hex,bubble_hex,0.133)}"
            )
        draw.rounded_rectangle(
                [(11.5*render_factor, 436.5*render_factor), (83*render_factor, 468.5*render_factor)],
                radius=22.5*render_factor,
                fill=f"#{bubble_hex}"
            )
        if additions == "PowerHelpOkay":
            draw.rounded_rectangle(
                    [(402.5*render_factor, 436.5*render_factor), (466.5*render_factor, 468.5*render_factor)],
                    radius=22.5*render_factor,
                    fill=f"#{bubble_hex}"
                )
        else:
            draw.rounded_rectangle(
                    [(302.5*render_factor, 436.5*render_factor), (366.5*render_factor, 468.5*render_factor)],
                    radius=22.5*render_factor,
                    fill=f"#{bubble_hex}"
                )
        draw.ellipse((535*render_factor, 436.5*render_factor,567*render_factor, 468.5*render_factor),fill=f"#{bubble_hex}")
        draw.ellipse((430.6*render_factor, 436.5*render_factor,462.6*render_factor, 468.5*render_factor),fill=f"#{bubble_hex}")

        draw.text(( 20*render_factor,441*render_factor), "POWER", font=inSmallerBubbleFont, fill=f"#{percentage_color(bg_hex,bubble_hex,0.593)}")
        draw.text(( 88*render_factor,439*render_factor), "SLEEP", font=inBubbleFont, fill=f"#{bubble_hex}")
        
        if additions == "PowerHelpOkay":
            draw.text(( 411.5*render_factor,441*render_factor), "MENU", font=inSmallerBubbleFont, fill=f"#{percentage_color(bg_hex,bubble_hex,0.593)}")
            draw.text(( 473*render_factor,439*render_factor), "HELP", font=inBubbleFont, fill=f"#{bubble_hex}")
        else:
            draw.text(( 311.5*render_factor,441*render_factor), "MENU", font=inSmallerBubbleFont, fill=f"#{percentage_color(bg_hex,bubble_hex,0.593)}")
            draw.text(( 373*render_factor,439*render_factor), "HELP", font=inBubbleFont, fill=f"#{bubble_hex}")

            draw.text(( 439.8*render_factor,436.2*render_factor), "B", font=singleLetterFont, fill=f"#{percentage_color(bg_hex,bubble_hex,0.593)}")
            draw.text(( 471.6*render_factor,439*render_factor), "BACK", font=inBubbleFont, fill=f"#{bubble_hex}")

        
        draw.text(( 543.6*render_factor,435.5*render_factor), "A", font=singleLetterFont, fill=f"#{percentage_color(bg_hex,bubble_hex,0.593)}")
        draw.text(( 573*render_factor,439*render_factor), "OKAY", font=inBubbleFont, fill=f"#{bubble_hex}")
    elif (muOSSystemName == "muxdevice" or muOSSystemName == "muxlaunch" or muOSSystemName == "muxconfig" or muOSSystemName == "muxinfo" or muOSSystemName == "muxapp"):
        menuHelperGuides = generateMenuHelperGuides(muOSSystemName,selected_font_path,bubble_hex,render_factor)

    elif show_file_counter_var.get() == 1:
        in_bubble_font_size = 19*render_factor
        inBubbleFont = ImageFont.truetype(selected_font_path, in_bubble_font_size)
        bbox = inBubbleFont.getbbox(fileCounter)
        text_width = bbox[2] - bbox[0]
        right_aligned_position = 620 * render_factor
        x = right_aligned_position - text_width
        y = 447 * render_factor
        draw.text(( x, y ), fileCounter, font=inBubbleFont, fill=f"#{bubble_hex}")    
    if folderName != None:
        if remove_brackets_var.get():
            folderName = remove_brackets_and_contents(folderName)
        if remove_square_brackets_var.get():
            folderName = remove_square_brackets_and_contents(folderName)
        if replace_hyphen_var.get():
            folderName = replace_hyphen_with_colon(folderName)
        if move_the_var.get():
            folderName = changeLocationOfThe(folderName)
        folderName = remove_dot_p8(folderName)


    if folderName != None and show_console_name_var.get():
        
        topTextFont = ImageFont.truetype(selected_font_path, 27*render_factor)

        bbox = topTextFont.getbbox(folderName)
        text_width = bbox[2] - bbox[0]

        text_x = (deviceScreenWidth*render_factor - text_width) / 2

        draw.text(( text_x,0*render_factor), folderName, font=topTextFont, fill=f"#{deselected_font_hex}")
    
    if muOSSystemName != "Folder" or not override_folder_box_art_padding_var.get():
        boxArtPadding = int(box_art_padding_entry.get()) * render_factor
    else:
        boxArtPadding = int(folder_box_art_padding_entry.get()) * render_factor

    textAlignment = None
    if muOSSystemName.startswith("mux"):
        if theme_alignment_var.get() == "Global":
            textAlignment = global_alignment_var.get()
        else:
            textAlignment = theme_alignment_var.get()
    else:
        if content_alignment_var.get() == "Global":
            textAlignment = global_alignment_var.get()
        else:
            textAlignment = content_alignment_var.get()

    if overlay_box_art_var.get() and textAlignment != "Centre":
        if listItems[workingIndex][1] == "File":
            if os.path.exists(os.path.join(box_art_directory_path.get(),muOSSystemName,"box",listItems[workingIndex][2]+".png")):
                originalBoxArtImage = Image.open(os.path.join(box_art_directory_path.get(),muOSSystemName,"box",listItems[workingIndex][2]+".png")).convert("RGBA")
                boxArtImage = originalBoxArtImage.resize((originalBoxArtImage.width*render_factor, originalBoxArtImage.height*render_factor), Image.LANCZOS)
                if textAlignment == "Left":
                    pasteLocation = (int((deviceScreenWidth*render_factor)-boxArtImage.width)-boxArtPadding,int(((deviceScreenHeight*render_factor)-boxArtImage.height)/2))
                else:
                    pasteLocation = (boxArtPadding,int(((deviceScreenHeight*render_factor)-boxArtImage.height)/2))
                
                boxArtWidth = originalBoxArtImage.width

                image.paste(boxArtImage,pasteLocation,boxArtImage)
                boxArtDrawn = True
        else:
            if os.path.exists(os.path.join(box_art_directory_path.get(),"Folder","box",listItems[workingIndex][2]+".png")):
                originalBoxArtImage = Image.open(os.path.join(box_art_directory_path.get(),"Folder","box",listItems[workingIndex][2]+".png")).convert("RGBA")
                boxArtImage = originalBoxArtImage.resize((originalBoxArtImage.width*render_factor, originalBoxArtImage.height*render_factor), Image.LANCZOS)
                
                if textAlignment == "Left":
                    pasteLocation = (int((deviceScreenWidth*render_factor)-boxArtImage.width)-boxArtPadding,int(((deviceScreenHeight*render_factor)-boxArtImage.height)/2))
                else:
                    pasteLocation = (boxArtPadding,int(((deviceScreenHeight*render_factor)-boxArtImage.height)/2))

                boxArtWidth = originalBoxArtImage.width


                image.paste(boxArtImage,pasteLocation,boxArtImage)
                boxArtDrawn = True

    font_size = (((deviceScreenHeight - footerHeight - headerHeight) * render_factor) / ItemsPerScreen) * textMF
    if override_font_size_var.get():
        try:
            font_size = int(custom_font_size_entry.get()) * render_factor
        except:
            font_size = (((deviceScreenHeight - footerHeight - headerHeight) * render_factor) / ItemsPerScreen) * textMF
    
    font = ImageFont.truetype(selected_font_path, font_size)

    availableHeight = ((deviceScreenHeight - headerHeight - footerHeight) * render_factor) / ItemsPerScreen

    smallestValidText_bbox = font.getbbox("_...")
    smallestValidTest_width = smallestValidText_bbox[2] - smallestValidText_bbox[0]

    for index, item in enumerate(listItems):
        noLettersCut = 0
        text_width = float('inf')
        if alternate_menu_names_var.get() and muOSSystemName.startswith("mux"):
            text = bidi_get_display(menuNameMap.get(item[0][:].lower(),item[0][:]))
        else:
            text = item[0][:]
        text_color = f"#{selected_font_hex}" if index == workingIndex else f"#{deselected_font_hex}"
        if boxArtDrawn and override_bubble_cut_var.get():
            if muOSSystemName == "Folder":
                maxBubbleLength = int(maxFoldersBubbleLengthVar.get())
            else:
                maxBubbleLength = int(maxGamesBubbleLengthVar.get())
        elif boxArtDrawn:
            maxBubbleLength = deviceScreenWidth - boxArtWidth - boxArtPadding - 5
        else:
            maxBubbleLength = deviceScreenWidth
        if maxBubbleLength*render_factor < textPadding*render_factor+smallestValidTest_width+rectanglePadding*render_factor+5*render_factor: #Make sure there won't be a bubble error
            maxBubbleLength = deviceScreenWidth

        if workingIndex == index:
            totalCurrentLength = (textPadding * render_factor + text_width + rectanglePadding * render_factor)
        else:
            totalCurrentLength = (textPadding * render_factor + text_width)
        while totalCurrentLength > (int(maxBubbleLength)*render_factor):
            if alternate_menu_names_var.get() and muOSSystemName.startswith("mux"):
                text = bidi_get_display(menuNameMap.get(item[0][:].lower(),item[0][:]))
            else:
                text = item[0][:]

            if remove_brackets_var.get():
                text = remove_brackets_and_contents(text)
            if remove_square_brackets_var.get():
                text = remove_square_brackets_and_contents(text)
            if replace_hyphen_var.get():
                text = replace_hyphen_with_colon(text)
            if move_the_var.get():
                text = changeLocationOfThe(text)
            text = remove_dot_p8(text)
            if noLettersCut>0:
                text = text[:-(noLettersCut+3)]
                text = text+"..."
            
            text_bbox = font.getbbox(text)
            text_width = text_bbox[2] - text_bbox[0]
            if workingIndex == index:
                totalCurrentLength = (textPadding * render_factor + text_width + rectanglePadding * render_factor)
            else:
                totalCurrentLength = (textPadding * render_factor + text_width)
            noLettersCut +=1
            if text  == "...":
                raise ValueError("'Cut bubble off at' too low\n\nPlease use a different custom 'cut bubble off' at value")
        
        if textAlignment == "Left":
            text_x = textPadding * render_factor
        elif textAlignment == "Right":
            text_x = (deviceScreenWidth-textPadding) * render_factor-text_width
        elif textAlignment == "Centre":
            text_x = ((deviceScreenWidth* render_factor-text_width)/2) 
        #text_y = headerHeight * render_factor + availableHeight * index

        
        rectangle_x0 = text_x - (rectanglePadding * render_factor)
        rectangle_y0 = headerHeight * render_factor + availableHeight * index
        rectangle_x1 = rectangle_x0 + rectanglePadding * render_factor + text_width + rectanglePadding * render_factor
        rectangle_y1 = headerHeight * render_factor + availableHeight * (index+1)
        middle_y = (rectangle_y0 + rectangle_y1) / 2
        ascent, descent = font.getmetrics()
        text_height = ascent + descent

        # Calculate the text's y-position by centering it vertically within the rectangle
        text_y = middle_y - (text_height / 2)

        corner_radius = availableHeight // 2

        if workingIndex == index:
            if transparent_text_var.get():
                draw_transparent.rounded_rectangle(
                    [(rectangle_x0, rectangle_y0), (rectangle_x1, rectangle_y1)],
                    radius=corner_radius,
                    fill=f"#{bubble_hex}"
                )
            else:
                draw.rounded_rectangle(
                    [(rectangle_x0, rectangle_y0), (rectangle_x1, rectangle_y1)],
                    radius=corner_radius,
                    fill=f"#{bubble_hex}"
                )   
        if transparent_text_var.get() and workingIndex == index:
            draw_transparent.text((text_x, text_y), text, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
        else:
            draw.text((text_x, text_y), text, font=font, fill=text_color)
            
    if transparent_text_var.get():
        image = Image.alpha_composite(image, transparent_text_image)
    if (muOSSystemName == "muxdevice" or muOSSystemName == "muxlaunch" or muOSSystemName == "muxconfig" or muOSSystemName == "muxinfo" or muOSSystemName == "muxapp"):
        image = Image.alpha_composite(image, menuHelperGuides)
    if showScrollBar:
        scrollBarHeight = (deviceScreenHeight - footerHeight - headerHeight) // numScreens
        rectangle_x0 = (deviceScreenWidth - scrollBarWidth) * render_factor
        rectangle_y0 = (headerHeight) * render_factor
        rectangle_x1 = (deviceScreenWidth) * render_factor
        rectangle_y1 = (deviceScreenHeight - footerHeight) * render_factor
        corner_radius = (scrollBarWidth // 2) * render_factor 

        draw.rounded_rectangle(
            [(rectangle_x0, rectangle_y0), (rectangle_x1, rectangle_y1)],
            radius=corner_radius,
            fill="darkgrey"
        )

        rectangle_x0 = (deviceScreenWidth - scrollBarWidth) * render_factor
        rectangle_y0 = (headerHeight + scrollBarHeight * screenIndex) * render_factor
        rectangle_x1 = (deviceScreenWidth) * render_factor
        rectangle_y1 = rectangle_y0 + scrollBarHeight * render_factor
        corner_radius = (scrollBarWidth // 2) * render_factor
        draw.rounded_rectangle(
            [(rectangle_x0, rectangle_y0), (rectangle_x1, rectangle_y1)],
            radius=corner_radius,
            fill=f"white"
        )
           
    return(image)


def ContinuousFolderImageGen(progress_bar,muOSSystemName, listItems, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDir, folderName = None):
    totalItems = len(listItems)
    scrollBarHeight = (deviceScreenHeight - footerHeight - headerHeight)

    

    for workingIndex, workingItem in enumerate(listItems):
        
        if workingItem[1] == "Directory" or also_games_var.get() or workingItem[1] == "Menu" or workingItem[1] == "ThemePreview":

            # Load the base image
            midIndexOfList = int((ItemsPerScreen-1)/2)
            if totalItems > ItemsPerScreen:
                if workingIndex < midIndexOfList:
                    startIndex = 0
                    focusIndex = workingIndex
                elif workingIndex > (totalItems- ItemsPerScreen)+midIndexOfList:
                    startIndex = totalItems - ItemsPerScreen
                    focusIndex = ItemsPerScreen-(totalItems-(workingIndex+1))-1
                else:
                    startIndex = workingIndex-midIndexOfList
                    focusIndex = midIndexOfList
                endIndex = min(startIndex+ItemsPerScreen,totalItems)
            else:
                startIndex = 0
                endIndex = totalItems
                focusIndex= workingIndex
            fileCounter = str(workingIndex + 1) + " / " + str(totalItems)

            image = generatePilImageVertical(progress_bar,
                                             focusIndex,
                                             muOSSystemName,
                                             listItems[startIndex:endIndex],
                                             additions,
                                             textPadding,
                                             rectanglePadding,
                                             ItemsPerScreen,
                                             bg_hex,
                                             selected_font_hex,
                                             deselected_font_hex,
                                             bubble_hex,
                                             render_factor,
                                             fileCounter=fileCounter,
                                             folderName = folderName)
                
            if muOSSystemName != "ThemePreview":
                image = image.resize((deviceScreenWidth, deviceScreenHeight), Image.LANCZOS)
                if workingItem[1] == "File":
                    directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/box/{workingItem[2]}.png")
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    image.save(f"{outputDir}/{muOSSystemName}/box/{workingItem[2]}.png")
                elif workingItem[1] == "Directory":
                    directory = os.path.dirname(f"{outputDir}/Folder/box/{workingItem[2]}.png")
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    image.save(f"{outputDir}/Folder/box/{workingItem[2]}.png")
                elif workingItem[1] == "Menu":
                    directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    image.save(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
            else:
                if workingIndex == 0:
                    image = image.resize((288, 216), Image.LANCZOS)
                    if workingItem[1] == "Menu":
                        image.save(os.path.join(internal_files_dir, "TempPreview.png"))


def PageFolderImageGen(progress_bar,muOSSystemName, listItems, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDir, folderName = None):
    
    totalItems = len(listItems)
    numScreens = math.ceil(totalItems / ItemsPerScreen)
    

    bg_rgb = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))

    for screenIndex in range(numScreens):
        startIndex = screenIndex * ItemsPerScreen
        endIndex = min(startIndex + ItemsPerScreen, totalItems)

        for workingIndex in range(startIndex, endIndex):
            workingItem = listItems[workingIndex]
            if workingItem[1] == "Directory" or also_games_var.get() or workingItem[1] == "Menu" or workingItem[1] == "ThemePreview":
                showScrollBar = False
                if numScreens > 1:  # Display Scroll Bar
                    showScrollBar = True
                fileCounter = str(workingIndex + 1) + " / " + str(totalItems)

                image = generatePilImageVertical(progress_bar,
                                                 workingIndex%ItemsPerScreen,
                                                 muOSSystemName,
                                                 listItems[startIndex:endIndex],
                                                 additions,
                                                 textPadding,
                                                 rectanglePadding,
                                                 ItemsPerScreen,
                                                 bg_hex,
                                                 selected_font_hex,
                                                 deselected_font_hex,
                                                 bubble_hex,render_factor,
                                                 scrollBarWidth=scrollBarWidth,
                                                 showScrollBar=showScrollBar,
                                                 numScreens=numScreens,
                                                 screenIndex=screenIndex,
                                                 fileCounter=fileCounter,
                                                 folderName = folderName)
                
                if muOSSystemName != "ThemePreview":
                    image = image.resize((deviceScreenWidth, deviceScreenHeight), Image.LANCZOS)
                    if workingItem[1] == "File":
                        directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/box/{workingItem[2]}.png")
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        image.save(f"{outputDir}/{muOSSystemName}/box/{workingItem[2]}.png")
                    elif workingItem[1] == "Directory":
                        directory = os.path.dirname(f"{outputDir}/Folder/box/{workingItem[2]}.png")
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        image.save(f"{outputDir}/Folder/box/{workingItem[2]}.png")
                    elif workingItem[1] == "Menu":
                        directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        image.save(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
                else:
                    if workingIndex == 0:
                        image = image.resize((288, 216), Image.LANCZOS)
                        if workingItem[1] == "Menu":
                            image.save(os.path.join(internal_files_dir, "TempPreview.png"))

def cut_out_image(original_image, logo_image, coordinates):
    x, y = coordinates
    
    # Ensure the images are in RGBA mode
    original_image = original_image.convert("RGBA")
    logo_image = logo_image.convert("RGBA")
    
    # Convert the images to NumPy arrays
    original_array = np.array(original_image)
    logo_array = np.array(logo_image)
    
    # Get the dimensions of the original and logo images
    original_height, original_width = original_array.shape[:2]
    logo_height, logo_width = logo_array.shape[:2]
    
    # Create a mask where the logo is not transparent
    logo_mask = logo_array[:, :, 3] > 0  # The alpha channel indicates transparency
    
    # Ensure the coordinates are within the bounds of the original image
    x_end = min(x + logo_width, original_width)
    y_end = min(y + logo_height, original_height)
    
    # Adjust the logo mask and arrays to fit within the bounds of the original image
    logo_mask = logo_mask[:y_end-y, :x_end-x]
    logo_alpha = logo_array[:y_end-y, :x_end-x, 3] / 255.0
    
    # Cut out the region of the original image where the logo is not transparent
    original_array[y:y_end, x:x_end, 3] = np.where(logo_mask, 
                                                   original_array[y:y_end, x:x_end, 3] * (1 - logo_alpha), 
                                                   original_array[y:y_end, x:x_end, 3])
    
    # Convert the modified NumPy array back to a Pillow image
    edited_image = Image.fromarray(original_array.astype('uint8'), 'RGBA')
    
    # Return the edited image
    return edited_image

def generatePilImageHorizontal(progress_bar,workingIndex, bg_hex, selected_font_hex,deselected_font_hex, bubble_hex,icon_hex,render_factor,transparent=False):
    progress_bar['value']+=1
    #print(f"progress_bar Max = {progress_bar['maximum']} | progress_bar Value = {progress_bar['value']} | {100*(int(progress_bar['value'])/int(progress_bar['maximum']))}%")
    bg_rgb = hex_to_rgb(bg_hex)

    # Create image

    if not transparent:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)

        if background_image != None:
            image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
    else:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), (0,0,0,0))


    

    exploreLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "explore.png"),icon_hex)
    favouriteLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "favourite.png"),icon_hex)
    historyLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "history.png"),icon_hex)
    appsLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "apps.png"),icon_hex)
   
    top_logo_size = (int((exploreLogoColoured.size[0]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5),
                     int((exploreLogoColoured.size[1]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5))
    
    exploreLogoColoured = exploreLogoColoured.resize((top_logo_size), Image.LANCZOS)
    favouriteLogoColoured = favouriteLogoColoured.resize((top_logo_size), Image.LANCZOS)
    historyLogoColoured = historyLogoColoured.resize((top_logo_size), Image.LANCZOS)
    appsLogoColoured = appsLogoColoured.resize((top_logo_size), Image.LANCZOS)
    
    combined_top_logos_width = exploreLogoColoured.size[0]+favouriteLogoColoured.size[0]+historyLogoColoured.size[0]+appsLogoColoured.size[0]

    icons_to_bubble_padding = min((deviceScreenHeight*0)/480,(deviceScreenWidth*0)/640)*render_factor ## CHANGE for adjustment

    bubble_height = min((deviceScreenHeight*36.3)/480,(deviceScreenWidth*36.3)/640)*render_factor ## CHANGE for adjustment

    screen_y_middle = (deviceScreenHeight*render_factor)/2

    combined_top_row_height = max(exploreLogoColoured.size[1],favouriteLogoColoured.size[1],historyLogoColoured.size[1],appsLogoColoured.size[1])+icons_to_bubble_padding+bubble_height

    top_row_icon_y = int(screen_y_middle-(combined_top_row_height/2))

    top_row_bubble_middle = int(screen_y_middle+(combined_top_row_height/2)-(bubble_height)/2)

    padding_between_top_logos = (deviceScreenWidth*render_factor-combined_top_logos_width)/(4+1) # 4 logos plus 1

    explore_middle = int(padding_between_top_logos+(exploreLogoColoured.size[0])/2)
    favourite_middle = int(padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+(favouriteLogoColoured.size[0])/2)
    history_middle = int(padding_between_top_logos+historyLogoColoured.size[0]+padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+(historyLogoColoured.size[0])/2)
    apps_middle = int(padding_between_top_logos+appsLogoColoured.size[0]+padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+historyLogoColoured.size[0]+padding_between_top_logos+(appsLogoColoured.size[0])/2)

    explore_logo_x = int(explore_middle-(exploreLogoColoured.size[0])/2)
    favourite_logo_x = int(favourite_middle-(favouriteLogoColoured.size[0])/2)
    history_logo_x = int(history_middle-(historyLogoColoured.size[0])/2)
    apps_logo_x = int(apps_middle-(appsLogoColoured.size[0])/2)

    image.paste(exploreLogoColoured,(explore_logo_x,top_row_icon_y),exploreLogoColoured)
    image.paste(favouriteLogoColoured,(favourite_logo_x,top_row_icon_y),favouriteLogoColoured)
    image.paste(historyLogoColoured,(history_logo_x,top_row_icon_y),historyLogoColoured)
    image.paste(appsLogoColoured,(apps_logo_x,top_row_icon_y),appsLogoColoured)

    draw = ImageDraw.Draw(image)
    if transparent_text_var.get():
        transparent_text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw_transparent = ImageDraw.Draw(transparent_text_image)
        transparency = 0

    if not use_alt_font_var.get():
        selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    else:
        if os.path.exists(alt_font_path.get()):
            selected_font_path = alt_font_path.get()
        else:
            selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    menuHelperGuides = generateMenuHelperGuides("muxlaunch",selected_font_path,bubble_hex,render_factor) 
    

    font_size = min((deviceScreenHeight*24)/480,(deviceScreenWidth*24)/640) * render_factor  ## CHANGE for adjustment
    font = ImageFont.truetype(selected_font_path, font_size)
    if workingIndex == 0:
        current_x_midpoint = explore_middle
    elif workingIndex == 1:
        current_x_midpoint = favourite_middle
    elif workingIndex == 2:
        current_x_midpoint = history_middle
    elif workingIndex == 3:
        current_x_midpoint = apps_middle
    else:
        current_x_midpoint = 104+(144*workingIndex)

    

    horizontalBubblePadding = min((deviceScreenHeight*40)/480,(deviceScreenWidth*40)/640)*render_factor  ## CHANGE for adjustment
    
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("content explorer", "Content"))
    else:
        textString = "Content"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    ascent, descent = font.getmetrics()
    text_height = ascent + descent

    text_y = top_row_bubble_middle - (text_height / 2)


    bubble_center_x =  explore_middle
    textColour = selected_font_hex if workingIndex == 0 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 0 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 0:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")
    
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("favourites", "Favourites"))
    else:
        textString = "Favourites"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  favourite_middle
    textColour = selected_font_hex if workingIndex == 1 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 1 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 1:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")

    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("history", "History"))
    else:
        textString = "History"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  history_middle
    textColour = selected_font_hex if workingIndex == 2 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 2 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 2:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("applications", "Utilities"))
    else:
        textString = "Utilities"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  apps_middle
    textColour = selected_font_hex if workingIndex == 3 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 3 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 3:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")

    

    if workingIndex == 4:
        infoLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "info.png"),selected_font_hex)
    else:
        infoLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "info.png"),deselected_font_hex)
    if workingIndex == 5:
        configLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "config.png"),selected_font_hex)
    else:
        configLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "config.png"),deselected_font_hex)
    if workingIndex == 6:
        rebootLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "reboot.png"),selected_font_hex)
    else:
        rebootLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "reboot.png"),deselected_font_hex)
    if workingIndex == 7:
        shutdownLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "shutdown.png"),selected_font_hex)
    else:
        shutdownLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "shutdown.png"),deselected_font_hex)
    
    bottom_logo_size = (int((infoLogoColoured.size[0]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5),
                     int((infoLogoColoured.size[1]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5))
    
    infoLogoColoured = infoLogoColoured.resize(bottom_logo_size, Image.LANCZOS)
    configLogoColoured = configLogoColoured.resize(bottom_logo_size, Image.LANCZOS)
    rebootLogoColoured = rebootLogoColoured.resize(bottom_logo_size, Image.LANCZOS)
    shutdownLogoColoured = shutdownLogoColoured.resize(bottom_logo_size, Image.LANCZOS)


    combined_bottom_logos_width = infoLogoColoured.size[0]+configLogoColoured.size[0]+rebootLogoColoured.size[0]+shutdownLogoColoured.size[0]

    circle_padding = min((deviceScreenHeight*15)/480,(deviceScreenWidth*15)/640)*render_factor ## CHANGE to adjust 

    combined_bottom_row_height = max(infoLogoColoured.size[1],configLogoColoured.size[1],rebootLogoColoured.size[1],shutdownLogoColoured.size[1])+circle_padding*2

    circle_radius = combined_bottom_row_height/2

    top_row_to_bottom_row_padding = min((deviceScreenHeight*20)/480,(deviceScreenWidth*20)/640)*render_factor ## CHANGE to adjust

    bottom_row_middle_y =  int(screen_y_middle+(combined_top_row_height/2)+top_row_to_bottom_row_padding+circle_radius)


    padding_from_screen_bottom_logos = deviceScreenWidth*(175/640)*render_factor ##CHANGE to adjust

    padding_between_bottom_logos = (deviceScreenWidth*render_factor-padding_from_screen_bottom_logos-combined_bottom_logos_width-padding_from_screen_bottom_logos)/(4-1) # 4 logos minus 1

    info_middle = int(padding_from_screen_bottom_logos+(infoLogoColoured.size[0])/2)
    config_middle = int(info_middle+(infoLogoColoured.size[0])/2+padding_between_bottom_logos+(configLogoColoured.size[0])/2)
    reboot_middle = int(config_middle+(configLogoColoured.size[0])/2+padding_between_bottom_logos+(rebootLogoColoured.size[0])/2)
    shutdown_middle = int(reboot_middle+(rebootLogoColoured.size[0])/2+padding_between_bottom_logos+(shutdownLogoColoured.size[0])/2)

    info_logo_x = int(info_middle-(infoLogoColoured.size[0])/2)
    config_logo_x = int(config_middle-(configLogoColoured.size[0])/2)
    reboot_logo_x = int(reboot_middle-(rebootLogoColoured.size[0])/2)
    shutdown_logo_x = int(shutdown_middle-(shutdownLogoColoured.size[0])/2)

    
    

    if workingIndex == 4:
        center_x = info_middle
        if transparent_text_var.get():
            draw_transparent.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
        else:
            draw.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
    elif workingIndex == 5:
        center_x = config_middle
        if transparent_text_var.get():
            draw_transparent.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
        else:
            draw.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
    elif workingIndex == 6:
        center_x = reboot_middle
        if transparent_text_var.get():
            draw_transparent.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
        else:
            draw.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
    elif workingIndex == 7:
        center_x = shutdown_middle
        if transparent_text_var.get():
            draw_transparent.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")
        else:
            draw.ellipse((int(center_x-circle_radius),int(bottom_row_middle_y-circle_radius),int(center_x+circle_radius),int(bottom_row_middle_y+circle_radius)),fill=f"#{bubble_hex}")

    info_logo_y = int(bottom_row_middle_y-(infoLogoColoured.size[1]/2))
    config_logo_y = int(bottom_row_middle_y-(configLogoColoured.size[1]/2))
    reboot_logo_y = int(bottom_row_middle_y-(rebootLogoColoured.size[1]/2))
    shutdown_logo_y = int(bottom_row_middle_y-(shutdownLogoColoured.size[1]/2))
    if transparent_text_var.get() and workingIndex >3:
        if workingIndex == 4:
            transparent_text_image = cut_out_image(transparent_text_image,infoLogoColoured,(info_logo_x,info_logo_y))
            image.paste(configLogoColoured,(config_logo_x,config_logo_y),configLogoColoured)
            image.paste(rebootLogoColoured,(reboot_logo_x,reboot_logo_y),rebootLogoColoured)
            image.paste(shutdownLogoColoured,(shutdown_logo_x,shutdown_logo_y),shutdownLogoColoured)
        elif workingIndex == 5:
            image.paste(infoLogoColoured,(info_logo_x,info_logo_y),infoLogoColoured)
            transparent_text_image = cut_out_image(transparent_text_image,configLogoColoured,(config_logo_x,config_logo_y))
            image.paste(rebootLogoColoured,(reboot_logo_x,reboot_logo_y),rebootLogoColoured)
            image.paste(shutdownLogoColoured,(shutdown_logo_x,shutdown_logo_y),shutdownLogoColoured)
        elif workingIndex == 6:
            image.paste(infoLogoColoured,(info_logo_x,info_logo_y),infoLogoColoured)
            image.paste(configLogoColoured,(config_logo_x,config_logo_y),configLogoColoured)
            transparent_text_image = cut_out_image(transparent_text_image,rebootLogoColoured,(reboot_logo_x,reboot_logo_y))
            image.paste(shutdownLogoColoured,(shutdown_logo_x,shutdown_logo_y),shutdownLogoColoured)
        elif workingIndex == 7:
            image.paste(infoLogoColoured,(info_logo_x,info_logo_y),infoLogoColoured)
            image.paste(configLogoColoured,(config_logo_x,config_logo_y),configLogoColoured)
            image.paste(rebootLogoColoured,(reboot_logo_x,reboot_logo_y),rebootLogoColoured)
            transparent_text_image = cut_out_image(transparent_text_image,shutdownLogoColoured,(shutdown_logo_x,shutdown_logo_y))
        
    else:
        image.paste(infoLogoColoured,(info_logo_x,info_logo_y),infoLogoColoured)
        image.paste(configLogoColoured,(config_logo_x,config_logo_y),configLogoColoured)
        image.paste(rebootLogoColoured,(reboot_logo_x,reboot_logo_y),rebootLogoColoured)
        image.paste(shutdownLogoColoured,(shutdown_logo_x,shutdown_logo_y),shutdownLogoColoured)

    if transparent_text_var.get():
        image = Image.alpha_composite(image, transparent_text_image)
    image = Image.alpha_composite(image, menuHelperGuides)
    
    return(image)

def generatePilImageAltHorizontal(progress_bar,workingIndex, bg_hex, selected_font_hex,deselected_font_hex, bubble_hex,icon_hex,render_factor,transparent=False):
    progress_bar['value']+=1
    #print(f"progress_bar Max = {progress_bar['maximum']} | progress_bar Value = {progress_bar['value']} | {100*(int(progress_bar['value'])/int(progress_bar['maximum']))}%")
    bg_rgb = hex_to_rgb(bg_hex)

    # Create image

    if not transparent:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)

        if background_image != None:
            image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
    else:
        image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), (0,0,0,0))


    top_to_bottom_row_padding = min((deviceScreenHeight*30)/480,(deviceScreenWidth*30)/640) * render_factor  ## CHANGE for adjustment
    

    exploreLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "explore.png"),icon_hex)
    favouriteLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "favourite.png"),icon_hex)
    historyLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "history.png"),icon_hex)
    appsLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "apps.png"),icon_hex)
   
    top_logo_size = (int((exploreLogoColoured.size[0]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5),
                     int((exploreLogoColoured.size[1]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5))
    
    exploreLogoColoured = exploreLogoColoured.resize((top_logo_size), Image.LANCZOS)
    favouriteLogoColoured = favouriteLogoColoured.resize((top_logo_size), Image.LANCZOS)
    historyLogoColoured = historyLogoColoured.resize((top_logo_size), Image.LANCZOS)
    appsLogoColoured = appsLogoColoured.resize((top_logo_size), Image.LANCZOS)
    
    combined_top_logos_width = exploreLogoColoured.size[0]+favouriteLogoColoured.size[0]+historyLogoColoured.size[0]+appsLogoColoured.size[0]

    icons_to_bubble_padding = min((deviceScreenHeight*0)/480,(deviceScreenWidth*0)/640)*render_factor ## CHANGE for adjustment

    bubble_height = min((deviceScreenHeight*36.3)/480,(deviceScreenWidth*36.3)/640)*render_factor ## CHANGE for adjustment

    screen_y_middle = (deviceScreenHeight*render_factor)/2

    combined_top_row_height = max(exploreLogoColoured.size[1],favouriteLogoColoured.size[1],historyLogoColoured.size[1],appsLogoColoured.size[1])+icons_to_bubble_padding+bubble_height

    top_row_icon_y = int(screen_y_middle-combined_top_row_height-(top_to_bottom_row_padding/2))

    top_row_bubble_middle = int(screen_y_middle-(bubble_height)/2-(top_to_bottom_row_padding/2))

    padding_between_top_logos = (deviceScreenWidth*render_factor-combined_top_logos_width)/(4+1) # 4 logos plus 1

    explore_middle_x = int(padding_between_top_logos+(exploreLogoColoured.size[0])/2)
    favourite_middle_x = int(padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+(favouriteLogoColoured.size[0])/2)
    history_middle_x = int(padding_between_top_logos+historyLogoColoured.size[0]+padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+(historyLogoColoured.size[0])/2)
    apps_middle_x = int(padding_between_top_logos+appsLogoColoured.size[0]+padding_between_top_logos+favouriteLogoColoured.size[0]+padding_between_top_logos+historyLogoColoured.size[0]+padding_between_top_logos+(appsLogoColoured.size[0])/2)

    explore_logo_x = int(explore_middle_x-(exploreLogoColoured.size[0])/2)
    favourite_logo_x = int(favourite_middle_x-(favouriteLogoColoured.size[0])/2)
    history_logo_x = int(history_middle_x-(historyLogoColoured.size[0])/2)
    apps_logo_x = int(apps_middle_x-(appsLogoColoured.size[0])/2)

    image.paste(exploreLogoColoured,(explore_logo_x,top_row_icon_y),exploreLogoColoured)
    image.paste(favouriteLogoColoured,(favourite_logo_x,top_row_icon_y),favouriteLogoColoured)
    image.paste(historyLogoColoured,(history_logo_x,top_row_icon_y),historyLogoColoured)
    image.paste(appsLogoColoured,(apps_logo_x,top_row_icon_y),appsLogoColoured)

    draw = ImageDraw.Draw(image)
    if transparent_text_var.get():
        transparent_text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw_transparent = ImageDraw.Draw(transparent_text_image)
        transparency = 0

    if not use_alt_font_var.get():
        selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    else:
        if os.path.exists(alt_font_path.get()):
            selected_font_path = alt_font_path.get()
        else:
            selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    menuHelperGuides = generateMenuHelperGuides("muxlaunch",selected_font_path,bubble_hex,render_factor) 
    

    font_size = min((deviceScreenHeight*24)/480,(deviceScreenWidth*24)/640) * render_factor  ## CHANGE for adjustment
    font = ImageFont.truetype(selected_font_path, font_size)
    if workingIndex == 0:
        current_x_midpoint = explore_middle_x
    elif workingIndex == 1:
        current_x_midpoint = favourite_middle_x
    elif workingIndex == 2:
        current_x_midpoint = history_middle_x
    elif workingIndex == 3:
        current_x_midpoint = apps_middle_x
    else:
        current_x_midpoint = 104+(144*workingIndex)

    

    horizontalBubblePadding = min((deviceScreenHeight*40)/480,(deviceScreenWidth*40)/640)*render_factor  ## CHANGE for adjustment
    
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("content explorer", "Content"))
    else:
        textString = "Content"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    ascent, descent = font.getmetrics()
    text_height = ascent + descent

    text_y = top_row_bubble_middle - (text_height / 2)


    bubble_center_x =  explore_middle_x
    textColour = selected_font_hex if workingIndex == 0 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 0 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 0:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")
    
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("favourites", "Favourites"))
    else:
        textString = "Favourites"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  favourite_middle_x
    textColour = selected_font_hex if workingIndex == 1 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 1 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(top_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(top_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 1:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")

    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("history", "History"))
    else:
        textString = "History"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  history_middle_x
    textColour = selected_font_hex if workingIndex == 2 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 2 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 2:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("applications", "Utilities"))
    else:
        textString = "Utilities"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  apps_middle_x
    textColour = selected_font_hex if workingIndex == 3 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 3 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((top_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((top_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 3:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")

    

    infoLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "alt-info.png"),icon_hex)
    configLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "alt-config.png"),icon_hex)
    rebootLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "alt-reboot.png"),icon_hex)
    shutdownLogoColoured = change_logo_color(os.path.join(internal_files_dir, "Assets", "Horizontal Logos", "alt-shutdown.png"),icon_hex)
   
    bottom_logo_size = (int((infoLogoColoured.size[0]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5),
                     int((infoLogoColoured.size[1]*render_factor*min(deviceScreenHeight/480,deviceScreenWidth/640))/5))
    
    infoLogoColoured = infoLogoColoured.resize((bottom_logo_size), Image.LANCZOS)
    configLogoColoured = configLogoColoured.resize((bottom_logo_size), Image.LANCZOS)
    rebootLogoColoured = rebootLogoColoured.resize((bottom_logo_size), Image.LANCZOS)
    shutdownLogoColoured = shutdownLogoColoured.resize((bottom_logo_size), Image.LANCZOS)
    
    combined_bottom_logos_width = infoLogoColoured.size[0]+configLogoColoured.size[0]+rebootLogoColoured.size[0]+shutdownLogoColoured.size[0]

    combined_bottom_row_height = max(infoLogoColoured.size[1],configLogoColoured.size[1],rebootLogoColoured.size[1],shutdownLogoColoured.size[1])+icons_to_bubble_padding+bubble_height

    bottom_row_icon_y = int(screen_y_middle+(top_to_bottom_row_padding/2))

    bottom_row_bubble_middle = int(screen_y_middle+(combined_bottom_row_height)-(bubble_height)/2+(top_to_bottom_row_padding/2))

    padding_between_bottom_logos = (deviceScreenWidth*render_factor-combined_bottom_logos_width)/(4+1) # 4 logos plus 1

    info_middle_x = int(padding_between_bottom_logos+(infoLogoColoured.size[0])/2)
    config_middle_x = int(info_middle_x+(infoLogoColoured.size[0])/2+padding_between_bottom_logos+(configLogoColoured.size[0])/2)
    reboot_middle_x = int(config_middle_x+(configLogoColoured.size[0])/2+padding_between_bottom_logos+(rebootLogoColoured.size[0])/2)
    shutdown_middle_x = int(reboot_middle_x+(rebootLogoColoured.size[0])/2+padding_between_bottom_logos+(shutdownLogoColoured.size[0])/2)

    info_logo_x = int(info_middle_x-(infoLogoColoured.size[0])/2)
    config_logo_x = int(config_middle_x-(configLogoColoured.size[0])/2)
    reboot_logo_x = int(reboot_middle_x-(rebootLogoColoured.size[0])/2)
    shutdown_logo_x = int(shutdown_middle_x-(shutdownLogoColoured.size[0])/2)

    image.paste(infoLogoColoured,(info_logo_x,bottom_row_icon_y),infoLogoColoured)
    image.paste(configLogoColoured,(config_logo_x,bottom_row_icon_y),configLogoColoured)
    image.paste(rebootLogoColoured,(reboot_logo_x,bottom_row_icon_y),rebootLogoColoured)
    image.paste(shutdownLogoColoured,(shutdown_logo_x,bottom_row_icon_y),shutdownLogoColoured)
    

    if workingIndex == 4:
        current_x_midpoint = info_middle_x
    elif workingIndex == 5:
        current_x_midpoint = config_middle_x
    elif workingIndex == 6:
        current_x_midpoint = reboot_middle_x
    elif workingIndex == 7:
        current_x_midpoint = shutdown_middle_x
    else:
        current_x_midpoint = 104+(144*workingIndex)

    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("information", "Info"))
    else:
        textString = "Info"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    ascent, descent = font.getmetrics()
    text_height = ascent + descent

    text_y = bottom_row_bubble_middle - (text_height / 2)


    bubble_center_x =  info_middle_x
    textColour = selected_font_hex if workingIndex == 4 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 4 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(bottom_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(bottom_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(bottom_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(bottom_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 4:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")
    
    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("configuration", "Config"))
    else:
        textString = "Config"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  config_middle_x
    textColour = selected_font_hex if workingIndex == 5 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 5 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(bottom_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(bottom_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int(bottom_row_bubble_middle-bubble_height/2)), ((current_x_midpoint+(bubbleLength/2)), int(bottom_row_bubble_middle+bubble_height/2))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 5:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")



    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("reboot device", "Reboot"))
    else:
        textString = "Reboot"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  reboot_middle_x
    textColour = selected_font_hex if workingIndex == 6 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 6 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((bottom_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((bottom_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((bottom_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((bottom_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 6:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")



    if alternate_menu_names_var.get():
        textString = bidi_get_display(menuNameMap.get("shutdown device", "Shutdown"))
    else:
        textString = "Shutdown"
    text_bbox = font.getbbox(textString)
    text_width = (text_bbox[2] - text_bbox[0])
    bubble_center_x =  shutdown_middle_x
    textColour = selected_font_hex if workingIndex == 7 else deselected_font_hex
    text_x = bubble_center_x - (text_width / 2)
    if workingIndex == 7 :
        bubbleLength = text_width+horizontalBubblePadding
        if transparent_text_var.get():
            draw_transparent.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((bottom_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((bottom_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
        else:
            draw.rounded_rectangle(
                [((current_x_midpoint-(bubbleLength/2)), int((bottom_row_bubble_middle-bubble_height/2))), ((current_x_midpoint+(bubbleLength/2)), int((bottom_row_bubble_middle+bubble_height/2)))],
                radius=(bubble_height/2),
                fill=f"#{bubble_hex}"
            )
    if transparent_text_var.get() and workingIndex == 7:
        draw_transparent.text((text_x, text_y), textString, font=font, fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    else:
        draw.text((text_x, text_y), textString, font=font, fill=f"#{textColour}")

    if transparent_text_var.get():
        image = Image.alpha_composite(image, transparent_text_image)
    image = Image.alpha_composite(image, menuHelperGuides)
    
    return(image)


def generatePilImageBootLogo(bg_hex,deselected_font_hex,bubble_hex,render_factor):
    bg_rgb = hex_to_rgb(bg_hex)
    image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)
    if use_custom_bootlogo_var.get():
        if os.path.exists(bootlogo_image_path.get()):
            bootlogo_image = Image.open(bootlogo_image_path.get())
            image.paste(bootlogo_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
            return image
    elif background_image != None:
        image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))

    draw = ImageDraw.Draw(image)
    transparent_text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw_transparent = ImageDraw.Draw(transparent_text_image)

    if not use_alt_font_var.get():
        selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    else:
        if os.path.exists(alt_font_path.get()):
            selected_font_path = alt_font_path.get()
        else:
            selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")

    mu_font_size = 130 * render_factor
    mu_font = ImageFont.truetype(selected_font_path, mu_font_size)
    os_font_size = 98 * render_factor
    os_font = ImageFont.truetype(selected_font_path, os_font_size)

    screen_x_middle, screen_y_middle = (deviceScreenWidth/2)*render_factor,(deviceScreenHeight/2)*render_factor

    from_middle_padding = 20*render_factor

    muText = "mu"

    osText = "OS"

    muTextBbox = mu_font.getbbox(muText)
    osTextBbox = os_font.getbbox(osText)

    muTextWidth = muTextBbox[2] - muTextBbox[0]
    muTextHeight = muTextBbox[3]-muTextBbox[1]
    mu_y_location = screen_y_middle-muTextHeight/2-muTextBbox[1]
    mu_x_location = screen_x_middle - from_middle_padding - muTextWidth

    osTextWidth = osTextBbox[2] - osTextBbox[0]
    osTextHeight = osTextBbox[3] - osTextBbox[1]
    os_y_location = screen_y_middle - osTextHeight / 2-osTextBbox[1]
    os_x_location = screen_x_middle + from_middle_padding

    bubble_x_padding = 30 * render_factor
    bubble_y_padding = 25 * render_factor
    bubble_x_mid_point = screen_x_middle + from_middle_padding + (osTextWidth / 2)
    bubble_width = bubble_x_padding + osTextWidth + bubble_x_padding
    bubble_height = bubble_y_padding + osTextHeight + bubble_y_padding
    transparency = 0
    
    draw_transparent.rounded_rectangle(
        [(bubble_x_mid_point-(bubble_width/2), screen_y_middle-(bubble_height/2)), (bubble_x_mid_point+(bubble_width/2), screen_y_middle+(bubble_height/2))],
        radius=bubble_height/2,
        fill=f"#{bubble_hex}"
    )

    draw.text((mu_x_location,mu_y_location), muText,font=mu_font, fill=f"#{deselected_font_hex}")
    draw_transparent.text((os_x_location,os_y_location),osText,font=os_font,fill=(*ImageColor.getrgb(f"#{bubble_hex}"), transparency))
    
    combined_image = Image.alpha_composite(image, transparent_text_image)

    return combined_image

def generatePilImageBootScreen(bg_hex,deselected_font_hex,icon_hex,display_text,render_factor,icon_path=None):
    bg_rgb = hex_to_rgb(bg_hex)
    image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)
    if background_image != None:
        image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
    
    draw = ImageDraw.Draw(image)

    if not use_alt_font_var.get():
        selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    else:
        if os.path.exists(alt_font_path.get()):
            selected_font_path = alt_font_path.get()
        else:
            selected_font_path = os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf")
    
    screen_x_middle, screen_y_middle = int((deviceScreenWidth/2)*render_factor),int((deviceScreenHeight/2)*render_factor)

    from_middle_padding = 0
    
    if icon_path != None:
        if os.path.exists(icon_path):
            from_middle_padding = 50*render_factor

            logoColoured = change_logo_color(icon_path,icon_hex)
            logoColoured = logoColoured.resize((int((logoColoured.size[0]/5)*render_factor),int((logoColoured.size[1]/5)*render_factor)), Image.LANCZOS)
            
            logo_y_location = int(screen_y_middle-logoColoured.size[1]/2-from_middle_padding)
            logo_x_location = int(screen_x_middle-logoColoured.size[0]/2)

            image.paste(logoColoured,(logo_x_location,logo_y_location),logoColoured)
            
    font_size = int(57.6 * render_factor)
    font = ImageFont.truetype(selected_font_path, font_size)

    displayText = display_text
    if alternate_menu_names_var.get():
        displayText = bidi_get_display(menuNameMap.get(display_text.lower(), display_text))

    

    textBbox = font.getbbox(displayText)

    textWidth = int(textBbox[2] - textBbox[0])
    textHeight = int(textBbox[3]-textBbox[1])
    y_location = int(screen_y_middle-textHeight/2-textBbox[1]+from_middle_padding)
    x_location = int(screen_x_middle - textWidth/2)

    draw.text((x_location,y_location), displayText, font=font, fill=f"#{deselected_font_hex}")

    
    return (image)

def generatePilImageDefaultScreen(bg_hex,render_factor):
    bg_rgb = hex_to_rgb(bg_hex)
    image = Image.new("RGBA", (deviceScreenWidth * render_factor, deviceScreenHeight * render_factor), bg_rgb)
    if background_image != None:
        image.paste(background_image.resize((deviceScreenWidth * render_factor, deviceScreenHeight * render_factor)), (0,0))
    return (image)

def HorizontalMenuGen(progress_bar,muOSSystemName, listItems, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex,icon_hex, render_factor, outputDir,variant):
    startIndex = 0
    endIndex = 8
    for workingIndex in range(startIndex, endIndex):
        workingItem = listItems[workingIndex]
        #image.save(os.path.join(script_dir,"Images for testing horizontal",f"{workingIndex}.png"))
        if variant == "Horizontal":
            image = generatePilImageHorizontal(progress_bar,workingIndex,bg_hex, selected_font_hex,deselected_font_hex,bubble_hex,icon_hex,render_factor)
        elif variant == "Alt-Horizontal":
           image = generatePilImageAltHorizontal(progress_bar,workingIndex,bg_hex, selected_font_hex,deselected_font_hex,bubble_hex,icon_hex,render_factor)
        else:
            raise ValueError("Something went wrong with your Main Menu Style")
        image = image.resize((deviceScreenWidth, deviceScreenHeight), Image.LANCZOS)
        if workingItem[1] == "File":
            directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/box/{workingItem[0]}.png")
            if not os.path.exists(directory):
                os.makedirs(directory)
            image.save(f"{outputDir}/{muOSSystemName}/box/{workingItem[0]}.png")
        elif workingItem[1] == "Directory":
            directory = os.path.dirname(f"{outputDir}/Folder/box/{workingItem[0]}.png")
            if not os.path.exists(directory):
                os.makedirs(directory)
            image.save(f"{outputDir}/Folder/box/{workingItem[0]}.png")
        elif workingItem[1] == "Menu":
            directory = os.path.dirname(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
            if not os.path.exists(directory):
                os.makedirs(directory)
            image.save(f"{outputDir}/{muOSSystemName}/{workingItem[2]}.png")
        if workingIndex == 0:
            image = image.resize((288, 216), Image.LANCZOS)
            if workingItem[1] == "Menu":
                image.save(os.path.join(internal_files_dir, "TempPreview.png"))

def remove_brackets_and_contents(text):
    # Remove contents within parentheses ()
    text = re.sub(r'\([^)]*\)', '', text)
    # Remove extra whitespace left by removal
    text = re.sub(r'\s+', ' ', text).strip()
    return text
def remove_square_brackets_and_contents(text):
    # Remove contents within square brackets []
    text = re.sub(r'\[[^\]]*\]', '', text)
    # Remove extra whitespace left by removal
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_dot_p8(text):
    if text.endswith('.p8'):
        return text[:-3]  # Remove the last 3 characters, which are ".p8"
    return text



def changeLocationOfThe(name):
    # Check if the name contains ', The'
    if ', The' in name:
        # Split the name into parts
        name = name.replace(', The', '')
        # Rearrange the parts with 'The ' at the beginning
        formatted_name = 'The ' + name
    else:
        formatted_name = name
    return formatted_name

def replace_hyphen_with_colon(text):
    return text.replace(' - ', ': ')

def getNameConversionList(file_path):
    if os.path.exists(name_json_path.get()):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except:
            return []
    return []

def getConsoleAssociationList():
    if os.path.exists(defaultConsoleAssociationsPath) and not os.path.exists(ConsoleAssociationsPath):
        shutil.copy(defaultConsoleAssociationsPath, ConsoleAssociationsPath)
    if os.path.exists(ConsoleAssociationsPath):
        try:
            with open(ConsoleAssociationsPath, 'r') as file:
                data = json.load(file)
            data = {key.lower(): value for key, value in data.items()}
            return data
        except:
            return []
    return []

def saveConsoleAssociationDict():
    with open(ConsoleAssociationsPath, 'w', newline='\n',encoding='utf-8') as json_file:
        json.dump(consoleMap, json_file, indent=2)         

def getAlternateMenuNameDict():
    if os.path.exists(alt_text_path.get()):
        try:
            
            with open(alt_text_path.get(), 'r', encoding='utf-8') as file:
                data = json.load(file)
            data = {key.lower(): value for key, value in data.items()}
            return data
        except:
            return getDefaultAlternateMenuNameData()
    elif os.path.exists(os.path.join(script_dir,alt_text_path.get())):
        try:
            with open(os.path.join(script_dir,alt_text_path.get()), 'r', encoding='utf-8') as file:
                data = json.load(file)
            data = {key.lower(): value for key, value in data.items()}
            return data
        except:
            return getDefaultAlternateMenuNameData()
    
    return getDefaultAlternateMenuNameData()

def getDefaultAlternateMenuNameData():
    defaultMenuNameMap = {}
    for section in menus2405_2:
        if section[0].startswith("mux"):
            for n in section[1]:
                defaultMenuNameMap[n[0].lower()] = n[0]
    
    defaultMenuNameMap["content explorer"] = "Games"
    defaultMenuNameMap["applications"] = "Utilities"
    defaultMenuNameMap["power"] = "POWER"
    defaultMenuNameMap["sleep"] = "SLEEP"
    defaultMenuNameMap["menu"] = "MENU"
    defaultMenuNameMap["help"] = "HELP"
    defaultMenuNameMap["back"] = "BACK"
    defaultMenuNameMap["okay"] = "OKAY"
    defaultMenuNameMap["confirm"] = "CONFIRM"
    defaultMenuNameMap["launch"] = "LAUNCH"
    defaultMenuNameMap["charging..."] = "Charging..."
    defaultMenuNameMap["loading..."] = "Loading..."
    defaultMenuNameMap["rebooting..."] = "Rebooting..."
    defaultMenuNameMap["shutting down..."] = "Shutting Down..."
    return defaultMenuNameMap

def list_directory_contents(directory_path):
    names_data = getNameConversionList(name_json_path.get())
    fileItemList = []
    directoryItemList = []
    itemList = []
    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            item_name, item_extension = os.path.splitext(item)
            item_type = "Directory" if os.path.isdir(item_path) else "File"
            if item_type == "Directory":
                if not(item_name[0] == "." or item_name[0] == "_") or show_hidden_files_var.get():
                    directoryItemList.append([item_name, item_type,item_name])
            else:
                if not(item_extension.lower() == ".pcm" or item_extension.lower() == ".msu" or item_extension.lower() == ".ips") and (not(item_name[0] == "." or item_name[0] == "_") or show_hidden_files_var.get()):
                    sort_name = names_data[item_name.lower()] if item_name.lower() in names_data else item_name+item_extension
                    display_name = names_data[item_name.lower()] if item_name.lower() in names_data else item_name
                    fileItemList.append([item_name, item_type, display_name, sort_name])
        if len(directoryItemList)+len(fileItemList):
            directoryItemList.sort(key=lambda x: x[0].lower())
            fileItemList.sort(key=lambda x: (x[3].lower()))

            for n in directoryItemList:
                itemList.append(n) # Display Name, File Type, File Name
            for n in fileItemList:
                itemList.append([n[2], n[1],n[0]])  # Display Name, File Type, File Name
            return itemList
        else:
            return []
    except Exception as e:
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            return f"ERROR: {e}\n{tb_str}"
        else:
            return f"ERROR: {e}"


def copy_contents(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path)
            else:
                copy_contents(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

def copy_contents_for_boxart_backup(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        
        # Determine the new destination path
        if os.path.isdir(src_path):
            dst_path = os.path.join(dst, item)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
                copy_contents_for_boxart_backup(src_path, dst_path)
            else:
                copy_contents_for_boxart_backup(src_path, dst_path)
        else:
            # Prefix "newboxart." to the file name
            if item[0]!=".":
                new_file_name = "newboxart." + item
                dst_path = os.path.join(dst, new_file_name)
                shutil.copy2(src_path, dst_path)


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        print(f"The folder {folder_path} does not exist.")

def remove_image_files_in_directory(directory):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file)[1].lower() in image_extensions:
                os.remove(file_path)

def get_console_name(file_path, directory_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(directory_path + ':='):
                return line.split('=')[1].strip()
    return None

def count_files_and_folders(directory):
    try:
        total_count = 0

        # Recursively walk through the directory
        for root, dirs, files in os.walk(directory):
            if not show_hidden_files_var.get():
                dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
                files = [f for f in files if not f.startswith('.') and not f.startswith('_')]
            #print(f"show hidden files: {show_hidden_files_var.get()} | Len dirs {len(dirs)} | Len files {len(files)}")
            total_count += len(dirs) + len(files)


        return total_count

    except FileNotFoundError:
        return "Directory not found."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"An error occurred: {e}"

def count_folders(directory):
    try:
        total_count = 0

        # Recursively walk through the directory
        for root, dirs, files in os.walk(directory):
            if not show_hidden_files_var.get():
                dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
                files = [f for f in files if not f.startswith('.') and not f.startswith('_')]
            if len(files)==0:
                total_count += len(dirs)


        return total_count

    except FileNotFoundError:
        return "Directory not found."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"An error occurred: {e}"

def traverse_and_generate_images(progress_bar, directory_path, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDirectory, input_queue, output_queue):
    items = list_directory_contents(directory_path)
    fileFound = False

    displayFolderName = None
    
    for item in items:
        if item[1] == "File":
            fileFound = True
            displayFolderName = os.path.basename(directory_path)
            break
    consoleName = "Folder"
    if fileFound and also_games_var.get() == 1: 
        folderName = os.path.basename(directory_path).lower()
        consoleName = consoleMap.get(folderName, None)
        if consoleName is None:
            input_queue.put(directory_path)
            consoleName = output_queue.get()
            consoleMap[folderName] = consoleName
            saveConsoleAssociationDict()

    if len(items) > 0 and consoleName != "SKIP":
        if not (fileFound and also_games_var.get() == 0):
            if page_by_page_var.get():
                PageFolderImageGen(progress_bar,consoleName, items, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDirectory, folderName = displayFolderName)
            else:
                ContinuousFolderImageGen(progress_bar, consoleName, items, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDirectory, folderName = displayFolderName)

    for item in items:
        item_name = item[0]
        item_type = item[1]
        if item_type == "Directory":
            new_path = os.path.join(directory_path, item_name)
            traverse_and_generate_images(progress_bar, new_path, additions, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, outputDirectory, input_queue, output_queue)

def select_console(directory_path):
    def on_select():
        selected_console.set(listbox.get(listbox.curselection()))
        root.quit()
    def on_skip():
        selected_console.set("SKIP")
        root.quit()

    root = tk.Tk()
    root.geometry("800x400") 
    root.title("Select Console")
    consoleOptions = ['Amstrad', 'Arcade', 'Arduboy', 'Atari 2600', 'Atari 5200',
            'Atari 7800', 'Atari Jaguar', 'Atari Lynx', 'Atari ST-STE-TT-Falcon', 'Bandai WonderSwan-Color', 
            'Cannonball', 'Cave Story', 'ChaiLove', 'ColecoVision', 'Commodore Amiga', 
            'Commodore C128', 'Commodore C64', 'Commodore CBM-II', 'Commodore PET', 'Commodore VIC-20', 
            'Dinothawr', 'Doom', 'DOS', 'External - Ports', 'Fairchild ChannelF', 
            'Flashback', 'Folder', 'Game Music Emu', 'GCE-Vectrex', 'Handheld Electronic - Game and Watch', 
            'Lowres NX', 'Mattel - Intellivision', 'Microsoft - MSX', 'Mr', 'MSX-SVI-ColecoVision-SG1000', 
            'NEC PC Engine', 'NEC PC Engine SuperGrafx', 'NEC PC-8000 - PC-8800 series', 'NEC PC-FX', 'NEC PC98', 
            'Nintendo DS', 'Nintendo Game Boy', 'Nintendo Game Boy Advance', 'Nintendo Game Boy Color', 'Nintendo N64', 
            'Nintendo NES-Famicom', 'Nintendo Pokemon Mini', 'Nintendo SNES-SFC', 'Nintendo Virtual Boy', 'Palm OS', 
            'Philips CDi', 'PICO-8', 'Quake', 'Rick Dangerous', 'RPG Maker 2000 - 2003', 
            'ScummVM', 'Sega 32X', 'Sega Atomiswave Naomi', 'Sega Dreamcast', 'Sega Game Gear', 
            'Sega Master System', 'Sega Mega CD - Sega CD', 'Sega Mega Drive - Genesis', 'Sega Saturn', 'Sharp X1', 
            'Sharp X68000', 'Sinclair ZX 81', 'Sinclair ZX Spectrum', 'SNK Neo Geo', 'SNK Neo Geo CD', 
            'SNK Neo Geo Pocket - Color', 'Sony PlayStation', 'Sony Playstation Portable', 'Texas Instruments TI-83', 'TIC-80', 
            'Uzebox', 'VeMUlator', 'Video Player', 'WASM-4', 'Watara Supervision', 'Wolfenstein 3D']

    label = tk.Label(root, text=f"What console on muOS is this folder associated with: [{os.path.basename(directory_path)}]?")
    label.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    listbox.grid(row=0, column=0, sticky='nsew')
    scrollbar.grid(row=0, column=1, sticky='ns')

    for option in consoleOptions:
        listbox.insert(tk.END, option)

    selected_console = tk.StringVar()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    skip_button = tk.Button(button_frame, text="SKIP", command=on_skip)
    skip_button.pack(side=tk.LEFT, padx=(0, 20))
    
    ok_button = tk.Button(button_frame, text="SELECT", command=on_select)
    ok_button.pack(side=tk.LEFT)
    
    root.mainloop()
    root.destroy()
    return selected_console.get()

def select_input_directory():
    roms_directory_path.set(filedialog.askdirectory())

def select_application_directory():
    application_directory_path.set(filedialog.askdirectory())

def select_box_art_directory():
    box_art_directory_path.set(filedialog.askdirectory())

def select_output_directory():
    catalogue_directory_path.set(filedialog.askdirectory())

def select_theme_directory():
    theme_directory_path.set(filedialog.askdirectory())
def select_am_theme_directory():
    am_theme_directory_path.set(filedialog.askdirectory())
def select_name_json_path():
    # File dialog to select a file, with specific types of files allowed
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],  # Only show .ini files
        title="Select name.json file"
    )
    
    # Check if the selected file is name.ini
    if file_path.endswith("name.json"):
        name_json_path.set(file_path)
    else:
        # Optionally show a warning or take other action if the wrong file is selected
        tk.messagebox.showerror("Invalid file", "Please select a file named 'name.json'")
def select_background_image_path():
    # File dialog to select a file, with specific types of files allowed
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png"),("Image Files", "*.jpg"),("Image Files", "*.jpeg"),("Image Files", "*.webp"),("Image Files", "*.gif"),("Image Files", "*.bmp")],  # Only show .png files
        title="Select background image file"
    )
    background_image_path.set(file_path)

def select_bootlogo_image_path():
    # File dialog to select a file, with specific types of files allowed
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png"),("Image Files", "*.jpg"),("Image Files", "*.jpeg"),("Image Files", "*.webp"),("Image Files", "*.gif"),("Image Files", "*.bmp")],  # Only show .png files
        title="Select bootlogo image file"
    )
    bootlogo_image_path.set(file_path)

def select_alt_font_path():
    # File dialog to select a file, with specific types of files allowed
    file_path = filedialog.askopenfilename(
        filetypes=[("Font Files", "*.ttf"), ("Font Files", "*.otf")],  # Only show font files
        title="Select font file"
    )
    alt_font_path.set(file_path)

def select_alt_text_path():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON", "*.json")],  # Only show font files
        title="Select Text Replacement file"
    )
    alt_text_path.set(file_path)


def remove_images():
    try:
        if catalogue_directory_path.get() != "":
            # Ask for confirmation before proceeding
            question = f"Are you sure you want to remove all images in this directory?\n{catalogue_directory_path.get()}"
            confirm = messagebox.askyesno("Confirmation", question)
            if confirm:
                remove_image_files_in_directory(catalogue_directory_path.get())
                messagebox.showinfo("Success", "Images successfully deleted.")
        else:
            raise ValueError("You Haven't Selected a Catalogue Folder")
    except Exception as e:
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An unexpected error occurred: {e}\n{tb_str}")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def backup_boxart():
    try:
        if am_theme_directory_path.get() == "":
            am_theme_dir = os.path.join(script_dir, "Generated Archive Manager Files")
        else:
            am_theme_dir = am_theme_directory_path.get()

        tempBackupCatalogueFolder = os.path.join(internal_files_dir,".TempBoxArtBackup","mnt","mmc","MUOS","info","catalogue")

        os.makedirs(os.path.join(internal_files_dir,".TempBoxArtBackup","opt"),exist_ok=True)

        shutil.copy2(os.path.join(internal_files_dir,"Template Box Art Backup","opt","update.sh"), os.path.join(internal_files_dir,".TempBoxArtBackup","opt","update.sh"))

        
        if os.path.exists(box_art_directory_path.get()):
            os.makedirs(tempBackupCatalogueFolder,exist_ok=True)
            copy_contents_for_boxart_backup(box_art_directory_path.get() ,tempBackupCatalogueFolder)
        
        shutil.make_archive(os.path.join(am_theme_dir, "Restore Backed Up Artwork"),"zip", os.path.join(internal_files_dir, ".TempBoxArtBackup"))
        
        if os.path.exists(os.path.join(internal_files_dir, ".TempBoxArtBackup")):
            delete_folder(os.path.join(internal_files_dir, ".TempBoxArtBackup"))
    except Exception as e:
        if os.path.exists(os.path.join(internal_files_dir, ".TempBoxArtBackup")):
            delete_folder(os.path.join(internal_files_dir, ".TempBoxArtBackup"))

def generate_images(progress_bar, loading_window, input_queue, output_queue):
    try:
        input_directory = roms_directory_path.get()
        output_directory = catalogue_directory_path.get()

        if not input_directory or not output_directory:
            raise ValueError("Input and output directory paths cannot be empty.")

        if not os.path.isdir(input_directory):
            raise ValueError(f"Invalid input directory: {input_directory}")
        
        progress_bar['value'] = 0
        progress_bar_max =0
        if also_games_var.get():
            totalRoms = count_files_and_folders(input_directory)
            progress_bar_max += totalRoms
        else:
            totalDirectories = count_folders(input_directory)
            progress_bar_max += totalDirectories
        progress_bar['maximum'] = progress_bar_max

        scrollBarWidth = int(scroll_bar_width_entry.get())
        textPadding = int(text_padding_entry.get())
        rectanglePadding = int(rectangle_padding_entry.get())
        bg_hex = background_hex_entry.get()
        selected_font_hex = selected_font_hex_entry.get()
        deselected_font_hex = deselected_font_hex_entry.get()
        bubble_hex = bubble_hex_entry.get()
        ItemsPerScreen = int(items_per_screen_entry.get())
        
        traverse_and_generate_images(progress_bar,input_directory, additions_Blank, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor,  output_directory,input_queue,output_queue)
        messagebox.showinfo("Success", "Images generated successfully.\nMake sure your box art setting is set to Fullscreen+Front!")
        loading_window.destroy()
    except ValueError as ve:
        loading_window.destroy()
        messagebox.showerror("Error", str(ve))

    except Exception as e:
        loading_window.destroy()
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An unexpected error occurred: {e}\n{tb_str}")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# INFO FOR BELOW LIST
#        FOLDER NAME      DISPLAYED NAME     FILE NAME

menus2405 = [["muxapps",[["Archive Manager","archive"],
                     ["Backup Manager","backup"],
                     ["Portmaster","portmaster"],
                     ["Retroarch","retroarch"],
                     ["Dingux Commander","dingux"],
                     ["Gmu Music Player","gmu"]]],
         ["muxconfig",[["General Settings","general"],
                     ["Theme Picker","theme"],
                     ["Wi-Fi Settings","network"],
                     ["Web Services","service"],
                     ["Date and Time","clock"],
                     ["Device Type","device"],
                     ["System Refresh","refresh"]]],
         ["muxdevice",[["RG35XX - H","rg35xx-h"],
                     ["RG35XX - Plus","rg35xx-plus"],
                     ["RG35XX - 2024","rg35xx-2024"]]],
         ["muxinfo",[["Input Tester","tester"],
                     ["System Details","system"],
                     ["Supporters","credit"]]],
         ["muxlaunch",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]],
         ["ThemePreview",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]]]

menus2405_1 = [["muxapp",[["Archive Manager","Archive Manager"],
                     ["Dingux Commander","Dingux Commander"],
                     ["GMU Music Player","GMU Music Player"],
                     ["PortMaster","PortMaster"],
                     ["RetroArch","RetroArch"],
                     ["Simple Terminal","Simple Terminal"],
                     ["Task Toolkit","Task Toolkit"]]],
         ["muxconfig",[["General Settings","general"],
                     ["Theme Picker","theme"],
                     ["Wi-Fi Settings","network"],
                     ["Web Services","service"],
                     ["Date and Time","clock"],
                     ["Device Type","device"]]],
         ["muxdevice",[["RG35XX - H","rg35xx-h"],
                     ["RG35XX - Plus","rg35xx-plus"],
                     ["RG35XX - SP","rg35xx-sp"],
                     ["RG35XX - 2024","rg35xx-2024"]]],
         ["muxinfo",[["Input Tester","tester"],
                     ["System Details","system"],
                     ["Supporters","credit"]]],
         ["muxlaunch",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]],
         ["ThemePreview",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]]]
menus2405_2 = [["muxapp",[["Archive Manager","Archive Manager"],
                     ["Dingux Commander","Dingux Commander"],
                     ["Flip Clock","Flip Clock"],
                     ["GMU Music Player","GMU Music Player"],
                     ["Moonlight","Moonlight"],
                     ["PortMaster","PortMaster"],
                     ["PPSSPP","PPSSPP"],
                     ["RetroArch","RetroArch"],
                     ["Simple Terminal","Simple Terminal"],
                     ["Task Toolkit","Task Toolkit"]]],
         ["muxconfig",[["General Settings","general"],
                     ["Theme Picker","theme"],
                     ["Wi-Fi Settings","network"],
                     ["Web Services","service"],
                     ["Date and Time","clock"],
                     ["Device Type","device"]]],
         ["muxdevice",[["RG35XX - H","rg35xx-h"],
                     ["RG35XX - Plus","rg35xx-plus"],
                     ["RG35XX - SP","rg35xx-sp"],
                     ["RG35XX - 2024","rg35xx-2024"]]],
         ["muxinfo",[["Input Tester","tester"],
                     ["System Details","system"],
                     ["Supporters","credit"]]],
         ["muxlaunch",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]],
         ["ThemePreview",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]]]
menus2405_3 = [["muxapp",[["Archive Manager","Archive Manager"],
                     ["Dingux Commander","Dingux Commander"],
                     ["Flip Clock","Flip Clock"],
                     ["GMU Music Player","GMU Music Player"],
                     ["Moonlight","Moonlight"],
                     ["PortMaster","PortMaster"],
                     ["PPSSPP","PPSSPP"],
                     ["RetroArch","RetroArch"],
                     ["Simple Terminal","Simple Terminal"],
                     ["Task Toolkit","Task Toolkit"]]],
         ["muxconfig",[["General Settings","general"],
                     ["Theme Picker","theme"],
                     ["Wi-Fi Settings","network"],
                     ["Web Services","service"],
                     ["Date and Time","clock"],
                     ["Device Type","device"]]],
         ["muxdevice",[["RG35XX - H","rg35xx-h"],
                     ["RG35XX - Plus","rg35xx-plus"],
                     ["RG35XX - SP","rg35xx-sp"],
                     ["RG35XX - 2024","rg35xx-2024"]]],
         ["muxinfo",[["Input Tester","tester"],
                     ["System Details","system"],
                     ["Supporters","credit"]]],
         ["muxlaunch",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]],
         ["ThemePreview",[["Content Explorer","explore"],
                     ["Favourites","favourite"],
                     ["History","history"],
                     ["Applications","apps"],
                     ["Information","info"],
                     ["Configuration","config"],
                     ["Reboot Device","reboot"],
                     ["Shutdown Device","shutdown"]]]]

def replace_in_file(file_path, search_string, replace_string):
    try:
        # Read the content of the file in binary mode
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        
        # Replace the occurrences of the search_string with replace_string in binary data
        search_bytes = search_string.encode()
        replace_bytes = replace_string.encode()
        new_contents = file_contents.replace(search_bytes, replace_bytes)
        
        # Write the new content back to the file in binary mode
        with open(file_path, 'wb') as file:
            file.write(new_contents)
    except Exception as e:
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An unexpected error occurred: {e}\n{tb_str}")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


def hex_to_rgb(hex_color,alpha = 1.0):
    # Convert hex to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (rgb[0], rgb[1], rgb[2], int(alpha * 255))

def rgb_to_hex(rgb_color):
    # Convert RGB to hex
    return '{:02x}{:02x}{:02x}'.format(*rgb_color)

def interpolate_color_component(c1, c2, factor):
    # Interpolate a single color component
    return int(c1 + (c2 - c1) * factor)

def percentage_color(hex1, hex2, percentage):
    # Convert hex colors to RGB
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    
    # Calculate the interpolated color for each component
    interp_rgb = tuple(interpolate_color_component(c1, c2, percentage) for c1, c2 in zip(rgb1, rgb2))
    
    # Convert interpolated RGB back to hex
    return rgb_to_hex(interp_rgb)

def generate_theme(progress_bar, loading_window):
    try:

        progress_bar['value'] = 0
        if main_menu_style_var.get() == "Vertical":
            progress_bar['maximum'] = 36
        elif main_menu_style_var.get() == "Horizontal":
            progress_bar['maximum'] = 28
        elif main_menu_style_var.get() == "Alt-Horizontal":
            progress_bar['maximum'] = 28
        else:
            raise ValueError("Something went wrong with your Main Menu Style")


        themeName = theme_name_entry.get()
        FillTempThemeFolder(progress_bar)
        if theme_directory_path.get() == "":
            theme_dir = os.path.join(script_dir, "Generated Theme")
        else:
            theme_dir = theme_directory_path.get()

        preview_dir = os.path.join(theme_dir,"preview")

        os.makedirs(preview_dir,exist_ok=True)

        shutil.make_archive(os.path.join(theme_dir, themeName),"zip", os.path.join(internal_files_dir, ".TempBuildTheme"))

        temp_preview_path = os.path.join(preview_dir, "TempPreview.png")
        if os.path.exists(temp_preview_path):
            os.remove(temp_preview_path)
        shutil.move(os.path.join(internal_files_dir, "TempPreview.png"), preview_dir)

        theme_preview_path = os.path.join(preview_dir, f"{themeName}.png")
        if os.path.exists(theme_preview_path):
            os.remove(theme_preview_path)

        os.rename(os.path.join(preview_dir,"TempPreview.png"), theme_preview_path)


        

        delete_folder(os.path.join(internal_files_dir, ".TempBuildTheme"))
        if os.path.exists(os.path.join(internal_files_dir, "TempPreview.png")):
            os.remove(os.path.join(internal_files_dir, "TempPreview.png"))
        if os.path.exists(os.path.join(theme_dir, "preview","TempPreview.png")):
            os.remove(os.path.join(theme_dir, "preview","TempPreview.png"))
        messagebox.showinfo("Success", "Theme generated successfully.")
        loading_window.destroy()
    except Exception as e:
        loading_window.destroy()
        if theme_directory_path.get() == "":
            theme_dir = os.path.join(script_dir, "Generated Theme")
        else:
            theme_dir = theme_directory_path.get()
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An unexpected error occurred: {e}\n{tb_str}")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        delete_folder(os.path.join(internal_files_dir, ".TempBuildTheme"))
        if os.path.exists(os.path.join(internal_files_dir, "TempPreview.png")):
            os.remove(os.path.join(internal_files_dir, "TempPreview.png"))
        if os.path.exists(os.path.join(theme_dir, "preview","TempPreview.png")):
            os.remove(os.path.join(theme_dir, "preview","TempPreview.png"))

def FillTempThemeFolder(progress_bar):
    legacyMethod = False
    if version_var.get() == "muOS 2405 BEANS" or version_var.get() == "muOS 2405.1 REFRIED BEANS" or version_var.get() == "muOS 2405.2 BAKED BEANS":
        legacyMethod = True
    else:
        if legacy_generation_var.get():
            legacyMethod =True
    

    scrollBarWidth = int(scroll_bar_width_entry.get())
    textPadding = int(text_padding_entry.get())
    rectanglePadding = int(rectangle_padding_entry.get())
    ItemsPerScreen = int(items_per_screen_entry.get())
    bg_hex = background_hex_entry.get()
    selected_font_hex = selected_font_hex_entry.get()
    deselected_font_hex = deselected_font_hex_entry.get()
    bubble_hex = bubble_hex_entry.get()
    icon_hex = icon_hex_entry.get()

    copy_contents(os.path.join(internal_files_dir, "Theme Shell"), os.path.join(internal_files_dir, ".TempBuildTheme"))

    newSchemeDir = os.path.join(internal_files_dir,".TempBuildTheme","scheme")
    os.makedirs(newSchemeDir, exist_ok=True)

    fontSize = 20
    if override_font_size_var.get():
        fontSize = int(customFontSizeVar.get())
    
    if legacyMethod:
        shutil.copy2(os.path.join(internal_files_dir,"Template Scheme","defaultlegacy.txt"),os.path.join(newSchemeDir,"default.txt"))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{bg_hex}", str(bg_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{selected_font_hex}", str(bubble_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{deselected_font_hex}", str(percentage_color(bubble_hex,selected_font_hex,0.5)))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{disabled_font_hex}", str(percentage_color(bg_hex,bubble_hex,0.25)))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{ImageOverlay}", str(include_overlay_var.get()))
        
        shutil.copy2(os.path.join(internal_files_dir,"Template Scheme","muxlegacy.txt"),os.path.join(newSchemeDir,"tempmux.txt"))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{bg_hex}", str(bg_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{selected_font_hex}", str(bubble_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{deselected_font_hex}", str(percentage_color(bubble_hex,bg_hex,0.5)))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{disabled_font_hex}", str(percentage_color(bg_hex,bubble_hex,0.25)))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{ImageOverlay}", str(include_overlay_var.get()))


        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxlaunch.txt"))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{ScrollDirection}", "0")
        if version_var.get() == "muOS 2405 BEANS":
            shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxapps.txt"))
        else:
            shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxapp.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxconfig.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxdevice.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxinfo.txt"))

        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{imageListAlpha}", str(255))
        if version_var.get() == "muOS 2405 BEANS":
            replace_in_file(os.path.join(newSchemeDir,"muxapps.txt"), "{imageListAlpha}", str(255))
        else:
            replace_in_file(os.path.join(newSchemeDir,"muxapp.txt"), "{imageListAlpha}", str(255))
        replace_in_file(os.path.join(newSchemeDir,"muxconfig.txt"), "{imageListAlpha}", str(255))
        replace_in_file(os.path.join(newSchemeDir,"muxdevice.txt"), "{imageListAlpha}", str(255))
        replace_in_file(os.path.join(newSchemeDir,"muxinfo.txt"), "{imageListAlpha}", str(255))

        if also_games_var.get():
            shutil.copy2(os.path.join(newSchemeDir,"default.txt"),os.path.join(newSchemeDir,"muxfavourite.txt"))
            shutil.copy2(os.path.join(newSchemeDir,"default.txt"),os.path.join(newSchemeDir,"muxhistory.txt"))

            replace_in_file(os.path.join(newSchemeDir,"muxfavourite.txt"), "{imageListAlpha}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"muxhistory.txt"), "{imageListAlpha}", str(0))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{imageListAlpha}", str(255))
        

        os.makedirs(os.path.join(internal_files_dir,".TempBuildTheme","image","wall"), exist_ok=True)

        if include_overlay_var.get():
            shutil.copy2(os.path.join(internal_files_dir,"Assets", "Overlays",f"{selected_overlay_var.get()}.png"),os.path.join(internal_files_dir,".TempBuildTheme","image","overlay.png"))

        os.remove(os.path.join(newSchemeDir,"tempmux.txt"))
    else:
        foreground_hex = deselected_font_hex
        midground_hex = percentage_color(bubble_hex,selected_font_hex,0.5)
        quarterground_hex = percentage_color(bg_hex,bubble_hex,0.25)

        shutil.copy2(os.path.join(internal_files_dir,"Template Scheme","default.txt"),os.path.join(newSchemeDir,"default.txt"))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{bg_hex}", str(bg_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{selected_font_hex}", str(foreground_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{deselected_font_hex}", str(midground_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{disabled_font_hex}", str(quarterground_hex))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"), "{ImageOverlay}", str(include_overlay_var.get()))
        replace_in_file(os.path.join(newSchemeDir,"default.txt"),"{imageListAlpha}", "255")
        replace_in_file(os.path.join(newSchemeDir,"default.txt"),"{ScrollDirection}", "0")

        
        
        shutil.copy2(os.path.join(internal_files_dir,"Template Scheme","muxlaunch.txt"),os.path.join(newSchemeDir,"muxlaunch.txt"))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{bg_hex}", str(bg_hex))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{selected_font_hex}", str(foreground_hex))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{deselected_font_hex}", str(midground_hex))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{disabled_font_hex}", str(quarterground_hex))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ImageOverlay}", str(include_overlay_var.get()))
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{imageListAlpha}", "255")

        if "Show icon on muxlaunch" == "":
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{font_list_icon_pad_top}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{list_default_glyph_alpha}", str(255))
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{list_focus_glyph_alpha}", str(255))
        else:
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{font_list_icon_pad_top}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{list_default_glyph_alpha}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"),"{list_focus_glyph_alpha}", str(0))

        shutil.copy2(os.path.join(internal_files_dir,"Template Scheme","muxthemed.txt"),os.path.join(newSchemeDir,"tempmux.txt"))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{bg_hex}", str(bg_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{foreground_hex}", str(foreground_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{midground_hex}", str(midground_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{quarterground_hex}", str(quarterground_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"), "{ImageOverlay}", str(include_overlay_var.get()))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{ScrollDirection}", "0")
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{imageListAlpha}", "255")
        # NEW ONES:
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{font_list_pad_left}",str(bubblePaddingVar.get()))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{font_list_pad_right}", str(bubblePaddingVar.get()))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{bubble_hex}", str(bubble_hex))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{bubble_alpha}", "255")
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_item_count}", str(itemsPerScreenVar.get()))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_padding_left}", str(int(textPaddingVar.get())-int(bubblePaddingVar.get())))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_padding_top}", str(headerHeight-44))


        
        if "Show Icon In Bubble" == "":
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{font_list_icon_pad_top}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{list_default_glyph_alpha}", str(255))
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{list_focus_glyph_alpha}", str(255))
        else:
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{font_list_icon_pad_top}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{list_default_glyph_alpha}", str(0))
            replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{list_focus_glyph_alpha}", str(0))
        content_height = deviceScreenHeight-headerHeight-int(footerHeightVar.get())
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_height}",str(content_height))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_width}", str(deviceScreenWidth-int(textPaddingVar.get())))
        bubble_height = (deviceScreenHeight-headerHeight-int(footerHeightVar.get()))/int(itemsPerScreenVar.get())
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{list_default_radius}", str(math.ceil(bubble_height/2)))
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{font_list_pad_top}", str(0))

        content_alignment_map = {"Left":0,"Centre":1,"Right":2}
        replace_in_file(os.path.join(newSchemeDir,"tempmux.txt"),"{content_alignment}", str(content_alignment_map[global_alignment_var.get()]))


        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxapp.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxconfig.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxdevice.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxinfo.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxfavourite.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxhistory.txt"))
        shutil.copy2(os.path.join(newSchemeDir,"tempmux.txt"),os.path.join(newSchemeDir,"muxplore.txt"))
        

        os.makedirs(os.path.join(internal_files_dir,".TempBuildTheme","image","wall"), exist_ok=True)

        if include_overlay_var.get():
            shutil.copy2(os.path.join(internal_files_dir,"Assets", "Overlays",f"{selected_overlay_var.get()}.png"),os.path.join(internal_files_dir,".TempBuildTheme","image","overlay.png"))

        os.remove(os.path.join(newSchemeDir,"tempmux.txt"))

    os.makedirs(os.path.join(internal_files_dir,".TempBuildTheme","font","panel"), exist_ok=True) #Font binaries stuff
    shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries","BPreplayBold-unhinted-20.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","default.bin"))
    if not legacyMethod:
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxapp.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxconfig.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxdevice.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxinfo.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxfavourite.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxhistory.bin"))
        shutil.copy2(os.path.join(internal_files_dir,"Assets","Font","Binaries",f"BPreplayBold-unhinted-{int(fontSize)}.bin"),os.path.join(internal_files_dir,".TempBuildTheme","font","panel","muxplore.bin"))


    if main_menu_style_var.get() == "Horizontal":
        if version_var.get() == "muOS 2405 BEANS" or version_var.get() == "muOS 2405.1 REFRIED BEANS" or version_var.get() == "muOS 2405.2 BAKED BEANS":
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "1") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
        else:
            if not "wrap":
                replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "2") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
            else:
                replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "4") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
    elif main_menu_style_var.get() == "Alt-Horizontal":
        if version_var.get() == "muOS 2405 BEANS" or version_var.get() == "muOS 2405.1 REFRIED BEANS" or version_var.get() == "muOS 2405.2 BAKED BEANS":
            replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "1") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
        else:
            if not "wrap":
                replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "2") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
            else:
                replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "4") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
    elif main_menu_style_var.get() == "Vertical":
        replace_in_file(os.path.join(newSchemeDir,"muxlaunch.txt"), "{ScrollDirection}", "0") ## ONLY DIFFERENCE BETWEEN THEMES IS MUXLAUNCH
    
    

    bootlogoimage = generatePilImageBootLogo(bgHexVar.get(),deselectedFontHexVar.get(),bubbleHexVar.get(),render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    bootlogoimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","bootlogo.bmp"), format='BMP')

    rotated_bootlogoimage = generatePilImageBootLogo(bgHexVar.get(),deselectedFontHexVar.get(),bubbleHexVar.get(),render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS).rotate(90,expand=True)
    rotated_bootlogoimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","bootlogo-alt.bmp"), format='BMP')

    chargingimage = generatePilImageBootScreen(bgHexVar.get(),
                                               deselectedFontHexVar.get(),
                                               iconHexVar.get(),
                                               "CHARGING...",
                                               render_factor,
                                               icon_path=os.path.join(internal_files_dir, "Assets", "ChargingLogo[5x].png")).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    chargingimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","wall","muxcharge.png"), format='PNG')

    loadingimage = generatePilImageBootScreen(bgHexVar.get(),
                                               deselectedFontHexVar.get(),
                                               iconHexVar.get(),
                                               "LOADING...",
                                               render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    loadingimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","wall","muxstart.png"), format='PNG')

    shutdownimage = generatePilImageBootScreen(bgHexVar.get(),
                                               deselectedFontHexVar.get(),
                                               iconHexVar.get(),
                                               "Shutting Down...",
                                               render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    shutdownimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","shutdown.png"), format='PNG')

    rebootimage = generatePilImageBootScreen(bgHexVar.get(),
                                               deselectedFontHexVar.get(),
                                               iconHexVar.get(),
                                               "Rebooting...",
                                               render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    rebootimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","reboot.png"), format='PNG')

    defaultimage = generatePilImageDefaultScreen(bgHexVar.get(),render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
    defaultimage.save(os.path.join(internal_files_dir,".TempBuildTheme","image","wall","default.png"), format='PNG')

    
    if False: ## Testing converting font in generator
        try:
            # Define the command
            command = [
                'lv_font_conv',
                '--bpp', '4',
                '--size', str(40),
                '--font', os.path.join(internal_files_dir, "Assets", "Font", "BPreplayBold-unhinted.otf"),
                '-r', '0x20-0x7F',
                '--format', 'bin',
                '--no-compress',
                '--no-prefilter',
                '-o', os.path.join(internal_files_dir, ".TempBuildTheme", "Assets", "font","default.bin")
            ]

            # Execute the command
            result = subprocess.run(command,shell=True )

        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    itemsList = []
    legacyMethod = False
    if version_var.get() == "muOS 2405 BEANS":
        workingMenus = menus2405
        legacyMethod = True
    elif version_var.get() == "muOS 2405.1 REFRIED BEANS":
        workingMenus = menus2405_1
        legacyMethod = True
    elif version_var.get() == "muOS 2405.2 BAKED BEANS":
        workingMenus = menus2405_2
        legacyMethod = True
    elif version_var.get() == "muOS 2405.3 COOL BEANS":
        workingMenus = menus2405_3
        if legacy_generation_var.get():
            legacyMethod = True
    else:
        raise ValueError("You Haven't Selected a muOS Version")
    rg28xxWorkingMenus = []
    for screen in workingMenus:
        if screen[0] == "muxconfig":
            rg28xxWorkingMenus.append(["muxconfig",[]])
            for item in screen[1]:
                if not(item[1] == "network" or item[1] == "service"): # Remove wifi related menu items 
                    rg28xxWorkingMenus[-1][1].append(item)
        else:
            rg28xxWorkingMenus.append(screen)


    if rg28xxVar.get():
        workingMenus = rg28xxWorkingMenus
    
    if not legacyMethod:
        workingMenus = [["muxlaunch",[["Content Explorer","explore"],
                                      ["Favourites","favourite"],
                                      ["History","history"],
                                      ["Applications","apps"],
                                      ["Information","info"],
                                      ["Configuration","config"],
                                      ["Reboot Device","reboot"],
                                      ["Shutdown Device","shutdown"]]],
                        ["ThemePreview",[["Content Explorer","explore"],
                                         ["Favourites","favourite"],
                                         ["History","history"],
                                         ["Applications","apps"],
                                         ["Information","info"],
                                         ["Configuration","config"],
                                         ["Reboot Device","reboot"],
                                         ["Shutdown Device","shutdown"]]]]

    for index, menu in enumerate(workingMenus):
        itemsList.append([])
        for item in menu[1]:
            itemsList[index].append([item[0],"Menu",item[1]]), 

    for index, menu in enumerate(workingMenus):
        if menu[0] == "muxdevice":
            if page_by_page_var.get():
                PageFolderImageGen(progress_bar,menu[0],itemsList[index],additions_powerHelpOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
            else:
                ContinuousFolderImageGen(progress_bar,menu[0],itemsList[index],additions_powerHelpOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
        elif menu[0] == "muxlaunch":
            if main_menu_style_var.get() == "Vertical":
                if page_by_page_var.get():
                    PageFolderImageGen(progress_bar,menu[0],itemsList[index],additions_PowerHelpBackOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
                else:
                    ContinuousFolderImageGen(progress_bar,menu[0],itemsList[index],additions_PowerHelpBackOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
            elif main_menu_style_var.get() == "Horizontal":
                HorizontalMenuGen(progress_bar,menu[0],itemsList[index], bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, icon_hex,render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"), variant = "Horizontal")
            elif main_menu_style_var.get() == "Alt-Horizontal":
                HorizontalMenuGen(progress_bar,menu[0],itemsList[index], bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, icon_hex,render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"), variant = "Alt-Horizontal")

        elif menu[0] == "ThemePreview":
                if main_menu_style_var.get() == "Vertical": 
                    if page_by_page_var.get():
                        PageFolderImageGen(progress_bar,menu[0],itemsList[index],additions_Preview,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
                    else:
                        ContinuousFolderImageGen(progress_bar,menu[0],itemsList[index],additions_Preview,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
        else:
            if page_by_page_var.get():
                PageFolderImageGen(progress_bar,menu[0],itemsList[index],additions_PowerHelpBackOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))
            else:
                ContinuousFolderImageGen(progress_bar,menu[0],itemsList[index],additions_PowerHelpBackOkay,scrollBarWidth,textPadding,rectanglePadding,ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor, os.path.join(internal_files_dir, ".TempBuildTheme","image","static"))

def select_alternate_menu_names():
    if os.path.exists(alt_text_path.get()):
        menu_names_grid = MenuNamesGrid(root, menuNameMap, alt_text_path.get())
    elif os.path.exists(os.path.join(script_dir,alt_text_path.get())):
        menu_names_grid = MenuNamesGrid(root, menuNameMap, os.path.join(script_dir,alt_text_path.get()))
    else:
        menu_names_grid = MenuNamesGrid(root, menuNameMap, os.path.join(script_dir,"AlternateMenuNames.json"))
    root.wait_window(menu_names_grid)
    on_change()

def generate_archive_manager(progress_bar, loading_window, input_queue, output_queue):
    try:
        scrollBarWidth = int(scroll_bar_width_entry.get())
        textPadding = int(text_padding_entry.get())
        rectanglePadding = int(rectangle_padding_entry.get())
        ItemsPerScreen = int(items_per_screen_entry.get())
        bg_hex = background_hex_entry.get()
        selected_font_hex = selected_font_hex_entry.get()
        deselected_font_hex = deselected_font_hex_entry.get()
        bubble_hex = bubble_hex_entry.get()
        amThemeName = am_theme_name_entry.get()
        roms_directory = roms_directory_path.get()
        

        progress_bar['value'] = 0
        progress_bar_max = 0
        if not am_ignore_cd_var.get():
            if also_games_var.get():
                totalRoms = count_files_and_folders(roms_directory)
                progress_bar_max += totalRoms
            else:
                totalRoms = count_folders(roms_directory)
                progress_bar_max += totalRoms
        
        if not am_ignore_theme_var.get():
            progress_bar_max += 28
        progress_bar['maximum'] = progress_bar_max

        if not am_ignore_cd_var.get():
            if not roms_directory:
                raise ValueError("ROMS directory paths cannot be empty.")

            if not os.path.isdir(roms_directory):
                raise ValueError(f"Invalid ROMS directory: {roms_directory}")
        
        if not am_ignore_theme_var.get():
            FillTempThemeFolder(progress_bar)
                    
        if not am_ignore_cd_var.get():
            if not os.path.exists(os.path.join(internal_files_dir, ".TempBuildAM","mnt","mmc","MUOS","info","catalogue")):
                os.makedirs(os.path.join(internal_files_dir, ".TempBuildAM","mnt","mmc","MUOS","info","catalogue"))
            output_directory = os.path.join(internal_files_dir, ".TempBuildAM","mnt","mmc","MUOS","info","catalogue")
            
            traverse_and_generate_images(progress_bar, roms_directory, additions_Blank, scrollBarWidth, textPadding, rectanglePadding, ItemsPerScreen, bg_hex, selected_font_hex, deselected_font_hex, bubble_hex, render_factor,  output_directory, input_queue, output_queue)

        if am_theme_directory_path.get() == "":
            am_theme_dir = os.path.join(script_dir, "Generated Archive Manager Files")
        else:
            am_theme_dir = am_theme_directory_path.get()

        if not am_ignore_theme_var.get():
            copy_contents(os.path.join(internal_files_dir, ".TempBuildTheme"),os.path.join(internal_files_dir, ".TempBuildAM","mnt","mmc","MUOS","theme","active"))

        os.makedirs(os.path.join(internal_files_dir,".TempBuildAM","mnt","boot"),exist_ok=True)
        
        if rg28xxVar.get():
            bootlogoimage = generatePilImageBootLogo(bgHexVar.get(),deselectedFontHexVar.get(),bubbleHexVar.get(),render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS).rotate(90,expand=True)
        else:
            bootlogoimage = generatePilImageBootLogo(bgHexVar.get(),deselectedFontHexVar.get(),bubbleHexVar.get(),render_factor).resize((deviceScreenWidth,deviceScreenHeight), Image.LANCZOS)
        bootlogoimage.save(os.path.join(internal_files_dir,".TempBuildAM","mnt","boot","bootlogo.bmp"), format='BMP')

        
        
        if os.path.exists(os.path.join(internal_files_dir, ".TempBuildAM")):
            shutil.make_archive(os.path.join(am_theme_dir, amThemeName),"zip", os.path.join(internal_files_dir, ".TempBuildAM"))

        if os.path.exists(os.path.join(internal_files_dir, ".TempBuildTheme")):
            delete_folder(os.path.join(internal_files_dir, ".TempBuildTheme"))
        if os.path.exists(os.path.join(internal_files_dir, ".TempBuildAM")):
            delete_folder(os.path.join(internal_files_dir, ".TempBuildAM"))
        if os.path.exists(os.path.join(internal_files_dir, "TempPreview.png")):
            os.remove(os.path.join(internal_files_dir, "TempPreview.png"))

        if not am_ignore_cd_var.get() or not am_ignore_theme_var.get():
            loading_window.destroy()
            messagebox.showinfo("Success", "Archive Manager File generated successfully.\nYou can now Activate the theme through Archive Manager")
    except Exception as e:
        loading_window.destroy()
        if theme_directory_path.get() == "":
            theme_dir = os.path.join(script_dir, "Generated Theme")
        else:
            theme_dir = theme_directory_path.get()
        delete_folder(os.path.join(internal_files_dir, ".TempBuildTheme"))
        delete_folder(os.path.join(internal_files_dir, ".TempBuildAM"))
        if os.path.exists(os.path.join(internal_files_dir, "TempPreview.png")):
            os.remove(os.path.join(internal_files_dir, "TempPreview.png"))
        if os.path.exists(os.path.join(theme_dir, "preview","TempPreview.png")):
            os.remove(os.path.join(theme_dir, "preview","TempPreview.png"))
        if advanced_error_var.get():
            tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            messagebox.showerror("Error", f"An unexpected error occurred: {e}\n{tb_str}")
        else:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def check_queue(root, input_queue, output_queue):
    try:
        directory_path = input_queue.get_nowait()
        consoleName = select_console(directory_path)
        output_queue.put(consoleName)
    except queue.Empty:
        pass
    root.after(100, check_queue, root, input_queue, output_queue)

class GridHelper:
    def __init__(self, root):
        self.root = root
        self.row = 0
        self.column = 0

    def add(self, widget, colspan=1, rowspan=1, next_row=False, **kwargs):
        widget.grid(row=self.row, column=self.column, columnspan=colspan, rowspan=rowspan, **kwargs)
        if next_row:
            self.row += 1
            self.column = 0
        else:
            self.column += colspan

class MenuNamesGrid(tk.Toplevel):
    def __init__(self, parent, data, AlternateMenuNamesPath):
        super().__init__(parent)
        self.title("Alternate Menu Names Editor")

        self.data = data
        self.entries = {}
        self.create_widgets()
        self.center_on_parent(parent)
        self.grab_set()

    def create_widgets(self):        
        # Split data into two halves
        items = list(self.data.items())
        half_index = len(items) // 2
        first_half = items[:half_index]
        second_half = items[half_index:]        

        # Populate the first half
        for i, (key, value) in enumerate(first_half):
            # Create read-only key label
            key_label = ttk.Label(self, text=key)
            key_label.grid(row=i, column=0, padx=5, pady=5, sticky='w')

            # Create editable value entry
            value_entry = ttk.Entry(self, width="50")
            value_entry.insert(0, value)
            value_entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.entries[key] = value_entry

        # Add space between the two halves
        spacer_label = ttk.Label(self, text="")
        spacer_label.grid(row=0, column=2, padx=20, pady=5)

        # Populate the second half
        for i, (key, value) in enumerate(second_half):
            # Create read-only key label
            key_label = ttk.Label(self, text=key)
            key_label.grid(row=i, column=3, padx=5, pady=5, sticky='w')

            # Create editable value entry
            value_entry = ttk.Entry(self, width="50")
            value_entry.insert(0, value)
            value_entry.grid(row=i, column=4, padx=5, pady=5, sticky='w')
            self.entries[key] = value_entry
            
        # Save button
        save_button = ttk.Button(self, text="Save", command=self.save)
        save_button.grid(row=max(len(first_half), len(second_half)), column=0, columnspan=5, pady=10)
    
    def center_on_parent(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2

        self.geometry(f'{self.winfo_width()}x{self.winfo_height()}+{x}+{y}')
    
    def save(self):
        for key, entry in self.entries.items():
            self.data[key] = entry.get()
        if os.path.exists(alt_text_path.get()):
            with open(alt_text_path.get(), 'w', newline='\n',encoding='utf-8') as json_file:
                json.dump(menuNameMap, json_file, indent=2)
        elif os.path.exists(os.path.join(script_dir,alt_text_path.get())):
            with open(os.path.join(script_dir,alt_text_path.get()), 'w', newline='\n',encoding='utf-8') as json_file:
                json.dump(menuNameMap, json_file, indent=2)
        else:
            with open(os.path.join(script_dir,"AlternateMenuNames.json"), 'w', newline='\n',encoding='utf-8') as json_file:
                json.dump(menuNameMap, json_file, indent=2)        
        
        self.grab_release()
        self.destroy()

def on_mousewheel(event,canvas):
    if platform.system() == 'Windows':
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif platform.system() == 'Darwin':
        canvas.yview_scroll(int(-1 * event.delta), "units")
    else:
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

def on_shiftmousewheel(event, canvas):
    if platform.system() == 'Windows':
        canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    elif platform.system() == 'Darwin':
        canvas.xview_scroll(int(-1 * event.delta), "units")
    else:
        if event.num == 4:
            canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas.xview_scroll(1, "units")
def update_slider_label():
    pass

def start_AM_task():
    # Create a new Toplevel window for the loading bar
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_window.geometry("300x100")
    
    # Create a Progressbar widget in the loading window
    progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=280, mode="determinate")
    progress_bar.pack(pady=20)
    
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    # Start the long-running task in a separate thread
    threading.Thread(target=generate_archive_manager, args=(progress_bar, loading_window, input_queue, output_queue)).start()

    # Check the queue periodically
    root.after(100, check_queue, root, input_queue, output_queue)

def start_images_task():
        # Create a new Toplevel window for the loading bar
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_window.geometry("300x100")
    
    # Create a Progressbar widget in the loading window
    progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=280, mode="determinate")
    progress_bar.pack(pady=20)
    
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    # Start the long-running task in a separate thread
    threading.Thread(target=generate_images, args=(progress_bar, loading_window, input_queue, output_queue)).start()

    # Check the queue periodically
    root.after(100, check_queue, root, input_queue, output_queue)

def start_theme_task():
        # Create a new Toplevel window for the loading bar
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_window.geometry("300x100")
    
    # Create a Progressbar widget in the loading window
    progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=280, mode="determinate")
    progress_bar.pack(pady=20)

    input_queue = queue.Queue()
    output_queue = queue.Queue()

    # Start the long-running task in a separate thread
    threading.Thread(target=generate_theme, args=(progress_bar, loading_window)).start()

    # Check the queue periodically
    root.after(100, check_queue, root, input_queue, output_queue)


def on_resize(event):
    global resize_id
    if resize_id is not None:
        root.after_cancel(resize_id)
    resize_id = root.after(200, on_change)  # Adjust the delay as needed

root = tk.Tk()
root.title("MinUI Theme Generator")
root.minsize(1080, 500)  # Set a minimum size for the window

# Get the screen height
screen_height = root.winfo_screenheight()
window_height = int(min(screen_height*0.9, 1720))

root.geometry(f"1280x{window_height}")  # Set a default size for the window

# Create the main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

resize_id = None

root.bind("<Configure>", on_resize)

subtitle_font = font.Font(family="Helvetica", size=10, weight="bold")
title_font = font.Font(family="Helvetica", size=14, weight="bold")

# Variables for user input
roms_directory_path = tk.StringVar()
application_directory_path = tk.StringVar()
name_json_path = tk.StringVar()
background_image_path = tk.StringVar()
bootlogo_image_path = tk.StringVar()
alt_font_path =  tk.StringVar()
alt_text_path = tk.StringVar()
box_art_directory_path = tk.StringVar()
catalogue_directory_path = tk.StringVar()
theme_directory_path = tk.StringVar()
am_theme_directory_path = tk.StringVar()
version_var = tk.StringVar()
global_alignment_var = tk.StringVar()
selected_overlay_var = tk.StringVar()
theme_alignment_var = tk.StringVar()
main_menu_style_var = tk.StringVar()
content_alignment_var = tk.StringVar()
also_games_var = tk.IntVar()
show_file_counter_var = tk.IntVar()
show_console_name_var = tk.IntVar()
show_hidden_files_var = tk.IntVar()
include_overlay_var = tk.IntVar()
alternate_menu_names_var = tk.IntVar()
remove_right_menu_guides_var = tk.IntVar()
remove_left_menu_guides_var = tk.IntVar()
override_bubble_cut_var = tk.IntVar()
page_by_page_var = tk.IntVar()
transparent_text_var = tk.IntVar()
override_font_size_var = tk.IntVar()
legacy_generation_var = tk.IntVar()
override_folder_box_art_padding_var = tk.IntVar()
use_alt_font_var = tk.IntVar()
use_custom_bootlogo_var = tk.IntVar()
rg28xxVar = tk.IntVar()
remove_brackets_var = tk.IntVar()
overlay_box_art_var = tk.IntVar(value=1)
remove_square_brackets_var = tk.IntVar()
replace_hyphen_var = tk.IntVar()
move_the_var = tk.IntVar()
am_ignore_theme_var = tk.IntVar()
am_ignore_cd_var = tk.IntVar()
advanced_error_var = tk.IntVar()

# Create a canvas and a vertical scrollbar

# Create the left frame with canvas and scrollbars
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True)

left_canvas = tk.Canvas(left_frame)
left_scrollbar_y = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
left_scrollable_frame = tk.Frame(left_canvas)

left_scrollable_frame.bind(
    "<Configure>",
    lambda e: left_canvas.configure(
        scrollregion=left_canvas.bbox("all")
    )
)

left_canvas.create_window((0, 0), window=left_scrollable_frame, anchor="nw")
left_canvas.configure(yscrollcommand=left_scrollbar_y.set)

left_canvas.pack(side="left", fill="both", expand=True)
left_scrollbar_y.pack(side="right", fill="y")

# Bind mouse wheel events based on the platform
if platform.system() == 'Darwin':
    left_canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, left_canvas))
    left_canvas.bind_all("<Shift-MouseWheel>", lambda event: on_shiftmousewheel(event, left_canvas))
else:
    left_canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, left_canvas))
    left_canvas.bind_all("<Shift-MouseWheel>", lambda event: on_shiftmousewheel(event, left_canvas))
    left_canvas.bind_all("<Button-4>", lambda event: on_mousewheel(event, left_canvas))  # For Linux
    left_canvas.bind_all("<Button-5>", lambda event: on_mousewheel(event, left_canvas))  # For Linux

# Create the grid helper
grid_helper = GridHelper(left_scrollable_frame)

is_dragging = False

def on_slider_change(value):
    global is_dragging
    is_dragging = True

    on_change()


# Create the GUI components
grid_helper.add(tk.Label(left_scrollable_frame, text="Adjust Preview Image Size:", fg='#00f'), colspan=3, sticky="w", next_row=True)


def on_slider_release(event):
    global is_dragging
    is_dragging = False
    on_change()

slider_length = 125

slider_length = 125
previewSideSlider = tk.Scale(left_scrollable_frame, from_=0, to=100, orient="horizontal", 
                             command=on_slider_change, showvalue=0, tickinterval=0, length=slider_length)
grid_helper.add(previewSideSlider, colspan=3, sticky="w", next_row=True)


# Bind mouse release event to the slider
previewSideSlider.bind("<ButtonRelease-1>", on_slider_release)


# Create the GUI components
grid_helper.add(tk.Label(left_scrollable_frame, text="[WARNING] PLEASE BACKUP YOUR WHOLE CATALOGUE FOLDER! CHOOSING SOME OPTIONS WILL OVERRIDE GAME BOX ART", fg='#f00'), colspan=3, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Configurations", font=title_font), colspan=3, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Global Configurations", font=subtitle_font), colspan=3, sticky="w", next_row=True)

# Define the StringVar variables
scrollBarWidthVar = tk.StringVar()
textPaddingVar = tk.StringVar()
bubblePaddingVar = tk.StringVar()
itemsPerScreenVar = tk.StringVar()
footerHeightVar = tk.StringVar()
boxArtPaddingVar = tk.StringVar()
folderBoxArtPaddingVar = tk.StringVar()
customFontSizeVar = tk.StringVar()
bgHexVar = tk.StringVar()
selectedFontHexVar = tk.StringVar()
deselectedFontHexVar = tk.StringVar()
bubbleHexVar = tk.StringVar()
iconHexVar = tk.StringVar()
maxGamesBubbleLengthVar = tk.StringVar()
maxFoldersBubbleLengthVar = tk.StringVar()
previewConsoleNameVar = tk.StringVar()


# Option for scrollBarWidth
grid_helper.add(tk.Label(left_scrollable_frame, text="Scroll Bar Width:"), sticky="w")
scroll_bar_width_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=scrollBarWidthVar)
grid_helper.add(scroll_bar_width_entry, next_row=True)

# Option for textPadding
grid_helper.add(tk.Label(left_scrollable_frame, text="Text Padding:"), sticky="w")
text_padding_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=textPaddingVar)
grid_helper.add(text_padding_entry, next_row=True)

# Option for rectanglePadding
grid_helper.add(tk.Label(left_scrollable_frame, text="Bubble Padding:"), sticky="w")
rectangle_padding_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=bubblePaddingVar)
grid_helper.add(rectangle_padding_entry, next_row=True)

# Option for ItemsPerScreen
grid_helper.add(tk.Label(left_scrollable_frame, text="Items Per Screen:"), sticky="w")
items_per_screen_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=itemsPerScreenVar)
grid_helper.add(items_per_screen_entry, next_row=True)

# Option for ItemsPerScreen
grid_helper.add(tk.Label(left_scrollable_frame, text="Footer Height:"), sticky="w")
footer_height_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=footerHeightVar)
grid_helper.add(footer_height_entry, next_row=True)

# Option for Background Colour
grid_helper.add(tk.Label(left_scrollable_frame, text="Background Hex Colour: #"), sticky="w")
background_hex_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=bgHexVar)
grid_helper.add(background_hex_entry, next_row=True)

# Option for Selected Font Hex Colour
grid_helper.add(tk.Label(left_scrollable_frame, text="Selected Font Hex Colour: #"), sticky="w")
selected_font_hex_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=selectedFontHexVar)
grid_helper.add(selected_font_hex_entry, next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Show Background Through Text", variable=transparent_text_var), colspan=3, sticky="w", next_row=True)

# Option for Deselected Font Hex Colour
grid_helper.add(tk.Label(left_scrollable_frame, text="Deselected Font Hex Colour: #"), sticky="w")
deselected_font_hex_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=deselectedFontHexVar)
grid_helper.add(deselected_font_hex_entry, next_row=True)

# Option for Bubble Hex Colour
grid_helper.add(tk.Label(left_scrollable_frame, text="Bubble Hex Colour: #"), sticky="w")
bubble_hex_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=bubbleHexVar)
grid_helper.add(bubble_hex_entry, next_row=True)

# Option for Icon Hex Colour
grid_helper.add(tk.Label(left_scrollable_frame, text="Icon Hex Colour: #"), sticky="w")
icon_hex_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=iconHexVar)
grid_helper.add(icon_hex_entry, next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Global Text Alignment"), sticky="w")
globalAlignmentOptions = ["Left", "Centre", "Right"]
global_alignment_option_menu = tk.OptionMenu(left_scrollable_frame, global_alignment_var, *globalAlignmentOptions)
grid_helper.add(global_alignment_option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Page by Page Scrolling", variable=page_by_page_var), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="[Optional] Override background colour with image"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=background_image_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_background_image_path), next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="*[Optional] Use Custom font:", variable=use_alt_font_var), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=alt_font_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_alt_font_path), next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame,text="*Use if text override characters not supported by default font",fg="#00f"),sticky="w",next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="[Optional] Override font size:", variable=override_font_size_var), sticky="w")
custom_font_size_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=customFontSizeVar)
grid_helper.add(custom_font_size_entry, next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Use Legacy Generation", variable=legacy_generation_var ), sticky="w")

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Theme Specific Configurations", font=subtitle_font), sticky="w", next_row=True)


grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Generating for the RG28XX", variable=rg28xxVar), sticky="w",next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Main Menu Style"), sticky="w")
MainMenuStyleOptions = ["Horizontal", "Vertical", "Alt-Horizontal"]
main_menu_style_option_menu = tk.OptionMenu(left_scrollable_frame, main_menu_style_var, *MainMenuStyleOptions)
grid_helper.add(main_menu_style_option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="[Optional] Custom Application Directory:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=application_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_application_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\MUOS\\application' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="muOS Version"), sticky="w")
options = ["muOS 2405 BEANS", "muOS 2405.1 REFRIED BEANS", "muOS 2405.2 BAKED BEANS", "muOS 2405.3 COOL BEANS"]
option_menu = tk.OptionMenu(left_scrollable_frame, version_var, *options)
grid_helper.add(option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Use Custom Bootlogo Image:", variable=use_custom_bootlogo_var), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=bootlogo_image_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_bootlogo_image_path), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Theme Text Alignment"), sticky="w")
themeAlignmentOptions = ["Global", "Left", "Centre", "Right"]
theme_alignment_option_menu = tk.OptionMenu(left_scrollable_frame, theme_alignment_var, *themeAlignmentOptions)
grid_helper.add(theme_alignment_option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Include Overlay", variable=include_overlay_var), sticky="w")

overlayOptions = ["muOS Default CRT Overlay", 
           "Grid_2px_10",
           "Grid_2px_20", 
           "Grid_2px_30", 
           "Grid_Thin_2px_10", 
           "Grid_Thin_2px_20", 
           "Grid_Thin_2px_30", 
           "Perfect_CRT-noframe", 
           "Perfect_CRT"]
overlay_option_menu = tk.OptionMenu(left_scrollable_frame, selected_overlay_var, *overlayOptions)
grid_helper.add(overlay_option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="[Optional] Use Custom Menu Text JSON File", variable=alternate_menu_names_var), sticky="w")

grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=alt_text_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_alt_text_path), next_row=True)

grid_helper.add(tk.Button(left_scrollable_frame, text="Edit Menu Names In JSON File", command=select_alternate_menu_names), sticky="w", next_row=True)


grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Remove Left Menu Helper Guides", variable=remove_left_menu_guides_var), sticky="w")
grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Remove Right Menu Helper Guides", variable=remove_right_menu_guides_var), colspan=3, sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Box Art Specific Configurations", font=subtitle_font), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Catalogue Directory with Box Art:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=box_art_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_box_art_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text=" - This can be your catalogue folder on your device, but I would recommend copying it off the device so you can use this tool multiple times.",fg="#00f"), colspan=3, sticky="w", next_row=True)

##BoxArtPadding
grid_helper.add(tk.Label(left_scrollable_frame, text="Box Art Right Padding:"), sticky="w")
box_art_padding_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=boxArtPaddingVar)
grid_helper.add(box_art_padding_entry, next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="[Optional] Folder Art Specific Padding:", variable=override_folder_box_art_padding_var), sticky="w")
folder_box_art_padding_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=folderBoxArtPaddingVar)
grid_helper.add(folder_box_art_padding_entry, next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Override Auto Cut Bubble off [Might want to use for fading box art]", variable=override_bubble_cut_var),colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text=" - [Games] Cut bubble off at (px):"), sticky="w")

max_games_bubble_length_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=maxGamesBubbleLengthVar)
grid_helper.add(max_games_bubble_length_entry, next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text=" - [Folders] Cut bubble off at (px):"), sticky="w")

max_folders_bubble_length_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=maxFoldersBubbleLengthVar)
grid_helper.add(max_folders_bubble_length_entry, next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text=" - This would usually be 640-width of your boxart",fg="#00f"), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Preview muOS Console name [Just for preview on the right]:"), sticky="w")
preview_console_name_entry = tk.Entry(left_scrollable_frame, width=50, textvariable=previewConsoleNameVar)
grid_helper.add(preview_console_name_entry, next_row=True)
grid_helper.add(tk.Button(left_scrollable_frame, text="Backup Box Art into Archive Manager File", command=backup_boxart, fg="#007B33"), sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Content Explorer Specific Configurations", font=subtitle_font), colspan=3, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Roms Input Directory:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=roms_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_input_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\ROMS' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="name.json file Directory:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=name_json_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_name_json_path), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\MUOS\\info\\name.json' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Content Explorer Text Alignment"), sticky="w")
contentAlignmentOptions = ["Global", "Left", "Centre", "Right"]
content_alignment_option_menu = tk.OptionMenu(left_scrollable_frame, content_alignment_var, *contentAlignmentOptions)
grid_helper.add(content_alignment_option_menu, colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Also Generate Theme for Game List *", variable=also_games_var), sticky="w")

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="[Experimental] Show hidden Content", variable=show_hidden_files_var), sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Merge with Box Art", variable=overlay_box_art_var), sticky="w")

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Replace ' - ' with ': '", variable=replace_hyphen_var), sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Remove ()", variable=remove_brackets_var), sticky="w")
grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Remove []", variable=remove_square_brackets_var), sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Put 'The' At the start, instead of the end ', The'", variable=move_the_var), sticky="w")

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Show File Counter **", variable=show_file_counter_var), sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Show Console Name at top", variable=show_console_name_var), sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="* [IMPORTANT] THIS WILL OVERRIDE YOUR GAME BOX ART... MAKE A BACKUP OF THE WHOLE CATALOGUE FOLDER.", fg='#f00'), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="* Games may also appear in the wrong order", fg='#0000ff'), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="** In order for File Counter to be visible box art must be set to 'Fullscreen + Front'", fg='#0000ff'), colspan=3, sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Generation", font=title_font), colspan=2, sticky="w", next_row=True)



grid_helper.add(tk.Label(left_scrollable_frame, text="Theme only generation [Recommended]", font=subtitle_font), colspan=2, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Theme Name:"), sticky="w")
theme_name_entry = tk.Entry(left_scrollable_frame, width=50)
grid_helper.add(theme_name_entry, next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Themes Output Directory:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=theme_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_theme_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\MUOS\\theme' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

# Generate button
grid_helper.add(tk.Button(left_scrollable_frame, text="Generate Theme", command=start_theme_task), sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Combined generation for Archive manager install [Legacy]", font=subtitle_font), colspan=2, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Make sure your box art setting is set to Fullscreen+Front for this!", font=subtitle_font,fg="#00f"), colspan=2, sticky="w", next_row=True)


grid_helper.add(tk.Label(left_scrollable_frame, text="Archive Manager Theme Name:"), sticky="w")
am_theme_name_entry = tk.Entry(left_scrollable_frame, width=50)
grid_helper.add(am_theme_name_entry, next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Archive Manager Output Directory:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=am_theme_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_am_theme_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\ARCHIVE' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Don't Generate Theme", variable=am_ignore_theme_var), colspan=1, sticky="w", next_row=False)
grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Don't Generate Content Explorer Theme", variable=am_ignore_cd_var), colspan=1, sticky="w", next_row=True)

# Generate button
grid_helper.add(tk.Button(left_scrollable_frame, text="Generate Archive Manager File", command=start_AM_task), sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Content explorer only generation [Legacy]", font=subtitle_font), colspan=2, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="Make sure your box art setting is set to Fullscreen+Front for this!", font=subtitle_font,fg="#00f"), colspan=2, sticky="w", next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Catalogue Directory on device:"), sticky="w")
grid_helper.add(tk.Entry(left_scrollable_frame, textvariable=catalogue_directory_path, width=50))
grid_helper.add(tk.Button(left_scrollable_frame, text="Browse...", command=select_output_directory), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="Should be '[root]:\\MUOS\\info\\catalogue' on your muOS SD Card, but it will let you select any folder."), colspan=3, sticky="w", next_row=True)

# Spacer row
grid_helper.add(tk.Label(left_scrollable_frame, text=""), next_row=True)

grid_helper.add(tk.Label(left_scrollable_frame, text="If you choose to generate the Game and Console Image files, to remove them you will need to", fg='#00f'), colspan=3, sticky="w", next_row=True)
grid_helper.add(tk.Label(left_scrollable_frame, text="remove all the files in your catalogue folder you can do this with the red button below.", fg='#00f'), colspan=2, sticky="w", next_row=True)

# Generate button
grid_helper.add(tk.Button(left_scrollable_frame, text="Generate Images", command=start_images_task), sticky="w")
grid_helper.add(tk.Button(left_scrollable_frame, text="Remove all images in Selected Catalogue Folder", command=remove_images, fg="#f00"), sticky="w", next_row=True)

grid_helper.add(tk.Checkbutton(left_scrollable_frame, text="Show Advanced Errors", variable=advanced_error_var), colspan=3, sticky="w", next_row=True)




# Create the right frame with canvas and scrollbars
right_frame = tk.Frame(main_frame)
right_frame.pack(side="left", fill="both", anchor="n")

right_canvas = tk.Canvas(right_frame)
right_scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
right_scrollable_frame = tk.Frame(right_canvas)



right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
right_canvas.configure(yscrollcommand=right_scrollbar.set)

right_canvas.pack(side="left", fill="both", expand=True)
right_scrollbar.pack(side="right", fill="y")


# Ensure the right frame expands only as needed

right_scrollable_frame.bind(
    "<Configure>",
    lambda e: right_frame.config(width=(right_canvas.bbox("all")[2] + right_scrollbar.winfo_width()))
)

right_frame.bind(
    "<Configure>",
    lambda e: right_canvas.configure(
        scrollregion=right_canvas.bbox("all")
    )
)

image_label1 = tk.Label(right_scrollable_frame)
image_label1.pack()

image_label2 = tk.Label(right_scrollable_frame)
image_label2.pack()

image_label3 = tk.Label(right_scrollable_frame)
image_label3.pack()

image_label4 = tk.Label(right_scrollable_frame)
image_label4.pack()

image_label5 = tk.Label(right_scrollable_frame)
image_label5.pack()

def update_image_label(image_label, pil_image):
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label.config(image=tk_image)
    image_label.image = tk_image
    #image_label.clear()
def remove_image_from_label(image_label):
    image_label.config(image='')


def get_current_image(image_label):
    # Retrieve the PhotoImage object from the label
    try:
        tk_image = image_label.image
    except:
        tk_image = None
    if tk_image is None:
        return None
    
    # Convert the PhotoImage object back to a PIL image
    width = tk_image.width()
    height = tk_image.height()
    pil_image = Image.new("RGB", (width, height))
    pil_image.paste(ImageTk.getimage(tk_image), (0, 0))

    return pil_image


def outline_image_with_inner_gap(image, outline_color=(255, 0, 0), outline_width=5, gap=5):
    # Calculate the size of the new image with the outline and the gap
    new_width = image.width + 2 * (outline_width + gap)
    new_height = image.height + 2 * (outline_width + gap)
    
    # Create a new image with the appropriate size and background color (optional)
    outlined_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    
    # Create a drawing context for the new image
    draw = ImageDraw.Draw(outlined_image)
    
    # Draw the outer rectangle for the red outline
    draw.rectangle(
        [0, 0, new_width - 1, new_height - 1],
        outline=outline_color,
        width=outline_width
    )
    
    # Paste the original image at the center of the new image, accounting for the outline width and gap
    outlined_image.paste(image, (outline_width + gap, outline_width + gap))

    final_image = outlined_image.resize((image.width, image.height), Image.LANCZOS)
    
    return final_image

valid_params = True


def updateMenusList(menusList, defaultList):
    if application_directory_path.get()!="" and os.path.exists(application_directory_path.get()): # muOS 2405.2
        newApplicationList = [[x[0],x[0]] for x in list_directory_contents(application_directory_path.get())]
        index = None
        for i, n in enumerate(menusList):
            if n[0] == "muxapp":
                index = i
                break
        if index!=None:
            menusList[index][1] = newApplicationList
    else:
        index = None
        for i, n in enumerate(menusList):
            if n[0] == "muxapp":
                index = i
                break
        if index!=None:
            menusList[index][1] = defaultList

def map_value(value, x_min, x_max, y_min, y_max):
    # Calculate the proportion of the value within the input range
    proportion = (value - x_min) / (x_max - x_min)
    
    # Map this proportion to the output range
    mapped_value = y_min + proportion * (y_max - y_min)
    
    return mapped_value

def on_change(*args):
    global menuNameMap
    menuNameMap = getAlternateMenuNameDict()
    try:
        if old_selected_overlay_var != selected_overlay_var.get():
            preview_overlay_image = Image.open(os.path.join(internal_files_dir, "Assets", "Overlays", f"{selected_overlay_var.get()}.png")).convert("RGBA")
    except:
        preview_overlay_image = Image.open(os.path.join(internal_files_dir, "Assets", "Overlays", f"{selected_overlay_var.get()}.png")).convert("RGBA")
    old_selected_overlay_var = selected_overlay_var.get()
    gameFolderName = "Game Boy"
    global footerHeight
    try:
        footerHeight = int(footer_height_entry.get())
    except:
        footerHeight = 55
    save_settings()
    config.save_config()
    global background_image

    if ("" != background_image_path.get()) and os.path.exists(background_image_path.get()):
        background_image = Image.open(background_image_path.get())
    else:
        background_image = None

    global menus2405
    global menus2405_1 ## NOT GLOBALS AHH SORRY HACKY SHOULD REMOVE
    global menus2405_2
    global menus2405_3

    menus2405_1_Default_list = [['Archive Manager', 'Archive Manager'], ['Dingux Commander', 'Dingux Commander'], ['GMU Music Player', 'GMU Music Player'], ['PortMaster', 'PortMaster'], ['RetroArch', 'RetroArch'], ['Simple Terminal', 'Simple Terminal'], ['Task Toolkit', 'Task Toolkit']]
    updateMenusList(menus2405_1, menus2405_1_Default_list)

    menus2405_2_Default_list = [['Archive Manager', 'Archive Manager'], ['Dingux Commander', 'Dingux Commander'], ['Flip Clock', 'Flip Clock'], ['GMU Music Player', 'GMU Music Player'], ['Moonlight', 'Moonlight'], ['PortMaster', 'PortMaster'], ['PPSSPP', 'PPSSPP'], ['RetroArch', 'RetroArch'], ['Simple Terminal', 'Simple Terminal'], ['Task Toolkit', 'Task Toolkit']]
    updateMenusList(menus2405_2, menus2405_2_Default_list)

    menus2405_3_Default_list = [['Archive Manager', 'Archive Manager'], ['Dingux Commander', 'Dingux Commander'], ['Flip Clock', 'Flip Clock'], ['GMU Music Player', 'GMU Music Player'], ['Moonlight', 'Moonlight'], ['PortMaster', 'PortMaster'], ['PPSSPP', 'PPSSPP'], ['RetroArch', 'RetroArch'], ['Simple Terminal', 'Simple Terminal'], ['Task Toolkit', 'Task Toolkit']]
    updateMenusList(menus2405_3, menus2405_3_Default_list)

    previewApplicationList = []
    if version_var.get() == "muOS 2405 BEANS":
        index = None
        for i, n in enumerate(menus2405):
            if n[0] == "muxapps":
                index = i
                break
        if index!=None:
            previewApplicationList = [[x[0],"menu",x[0]] for x in menus2405[index][1]]
    elif version_var.get() == "muOS 2405.1 REFRIED BEANS":
        index = None
        for i, n in enumerate(menus2405_1):
            if n[0] == "muxapp":
                index = i
                break
        if index!=None:
            previewApplicationList = [[x[0],"menu",x[0]] for x in menus2405_1[index][1]]
    elif version_var.get() == "muOS 2405.2 BAKED BEANS":
        index = None
        for i, n in enumerate(menus2405_2):
            if n[0] == "muxapp":
                index = i
                break
        if index!=None:
            previewApplicationList = [[x[0],"menu",x[0]] for x in menus2405_2[index][1]]
    elif version_var.get() == "muOS 2405.3 COOL BEANS":
        index = None
        for i, n in enumerate(menus2405_3):
            if n[0] == "muxapp":
                index = i
                break
        if index!=None:
            previewApplicationList = [[x[0],"menu",x[0]] for x in menus2405_3[index][1]]

    global valid_params
    
    fakeprogressbar={'value':0}
    fakeprogressbar['maximum']=1

    previewRenderFactor = 1

    if root.winfo_height() < 100:
        preview_size = [int(deviceScreenWidth/2),int(deviceScreenHeight/2)]
    else:
        imagesOnScreen = 5
        if main_menu_style_var.get() == "Vertical":
            imagesOnScreen = 4

        preview_multiplier = (root.winfo_height()/map_value(previewSideSlider.get(),0,100,imagesOnScreen,1))/deviceScreenHeight
        global is_dragging
        if is_dragging:
            previewRenderFactor = 1
        else:
            previewRenderFactor = int(preview_multiplier*(1/0.64)+1) # Affectively anti aliasing in the preview
            

        preview_size = [deviceScreenWidth*preview_multiplier,deviceScreenHeight*preview_multiplier]
        betweenImagePadding = 4
        oldHeight = preview_size[1]
        preview_size[1] -= betweenImagePadding+betweenImagePadding/map_value(previewSideSlider.get(),0,100,imagesOnScreen,1)
        preview_size[0] = (preview_size[0]*preview_size[1])/(oldHeight)
        preview_size[0],preview_size[1] = int(preview_size[0]),int(preview_size[1])

    # This function will run whenever any traced variable changes
    try:
        consoleName = consoleMap.get(previewConsoleNameVar.get().lower(), previewConsoleNameVar.get())
        previewItemList = [['Content Explorer', 'Menu', 'explore'], ['Favourites', 'Menu', 'favourite'], ['History', 'Menu', 'history'], ['Applications', 'Menu', 'apps'], ['Information', 'Menu', 'info'], ['Configuration', 'Menu', 'config'], ['Reboot Device', 'Menu', 'reboot'], ['Shutdown Device', 'Menu', 'shutdown']]
        previewGameItemList = [['4-in-1 Fun Pak [Version 1] (USA, Europe)', 'File', '4-in-1 Fun Pak [Version 1] (USA, Europe)'], ['4-in-1 Funpak - Volume II (USA, Europe)', 'File', '4-in-1 Funpak - Volume II (USA, Europe)'], ['A-mazing Tater (USA)', 'File', 'A-mazing Tater (USA)'], ['Addams Family, The (USA)', 'File', 'Addams Family, The (USA)'], ["Addams Family, The - Pugsley's Scavenger Hunt (USA, Europe) [Revision]", 'File', "Addams Family, The - Pugsley's Scavenger Hunt (USA, Europe) [Revision]"], ['Adventure Island (USA, Europe)', 'File', 'Adventure Island (USA, Europe)'], ['Adventure Island II - Aliens in Paradise (USA, Europe)', 'File', 'Adventure Island II - Aliens in Paradise (USA, Europe)'], ['Adventures of Rocky and Bullwinkle and Friends, The (USA)', 'File', 'Adventures of Rocky and Bullwinkle and Friends, The (USA)'], ['Adventures of Star Saver, The (USA, Europe)', 'File', 'Adventures of Star Saver, The (USA, Europe)'], ['Aerostar (USA, Europe)', 'File', 'Aerostar (USA, Europe)'], ['Aladdin (USA) (SGB Enhanced)', 'File', 'Aladdin (USA) (SGB Enhanced)'], ['Alfred Chicken (USA)', 'File', 'Alfred Chicken (USA)'], ['Alien 3 (USA, Europe)', 'File', 'Alien 3 (USA, Europe)'], ['Alien vs Predator - The Last of His Clan (USA)', 'File', 'Alien vs Predator - The Last of His Clan (USA)'], ['All-Star Baseball 99 (USA)', 'File', 'All-Star Baseball 99 (USA)'], ['Altered Space - A 3-D Alien Adventure (USA)', 'File', 'Altered Space - A 3-D Alien Adventure (USA)'], ['Amazing Penguin (USA, Europe)', 'File', 'Amazing Penguin (USA, Europe)'], ['Amazing Spider-Man, The (USA, Europe)', 'File', 'Amazing Spider-Man, The (USA, Europe)'], ['Animaniacs (USA) (SGB Enhanced)', 'File', 'Animaniacs (USA) (SGB Enhanced)'], ['Arcade Classic No. 1 - Asteroids & Missile Command (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 1 - Asteroids & Missile Command (USA, Europe) (SGB Enhanced)'], ['Arcade Classic No. 2 - Centipede & Millipede (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 2 - Centipede & Millipede (USA, Europe) (SGB Enhanced)'], ['Arcade Classic No. 3 - Galaga & Galaxian (USA) (SGB Enhanced)', 'File', 'Arcade Classic No. 3 - Galaga & Galaxian (USA) (SGB Enhanced)'], ['Arcade Classic No. 4 - Defender & Joust (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 4 - Defender & Joust (USA, Europe) (SGB Enhanced)'], ['Arcade Classics - Super Breakout & Battlezone (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classics - Super Breakout & Battlezone (USA, Europe) (SGB Enhanced)'], ['Asteroids (USA, Europe)', 'File', 'Asteroids (USA, Europe)'], ['Atomic Punk (USA)', 'File', 'Atomic Punk (USA)'], ['Attack of the Killer Tomatoes (USA, Europe)', 'File', 'Attack of the Killer Tomatoes (USA, Europe)'], ['Avenging Spirit (USA, Europe)', 'File', 'Avenging Spirit (USA, Europe)'], ['Balloon Kid (USA, Europe)', 'File', 'Balloon Kid (USA, Europe)'], ['Barbie - Game Girl (USA, Europe)', 'File', 'Barbie - Game Girl (USA, Europe)'], ["Bart Simpson's Escape from Camp Deadly (USA, Europe)", 'File', "Bart Simpson's Escape from Camp Deadly (USA, Europe)"], ['Bases Loaded for Game Boy (USA)', 'File', 'Bases Loaded for Game Boy (USA)'], ['Batman - Return of the Joker (USA, Europe)', 'File', 'Batman - Return of the Joker (USA, Europe)'], ['Batman - The Animated Series (USA, Europe)', 'File', 'Batman - The Animated Series (USA, Europe)'], ['Batman Forever (USA, Europe)', 'File', 'Batman Forever (USA, Europe)'], ['Battle Arena Toshinden (USA) (SGB Enhanced)', 'File', 'Battle Arena Toshinden (USA) (SGB Enhanced)'], ['Battle Bull (USA)', 'File', 'Battle Bull (USA)'], ['Battle Unit Zeoth (USA, Europe)', 'File', 'Battle Unit Zeoth (USA, Europe)'], ['Battleship (USA, Europe)', 'File', 'Battleship (USA, Europe)'], ['Battletoads (USA, Europe)', 'File', 'Battletoads (USA, Europe)'], ["Battletoads in Ragnarok's World (USA)", 'File', "Battletoads in Ragnarok's World (USA)"], ['Battletoads-Double Dragon (USA)', 'File', 'Battletoads-Double Dragon (USA)'], ['Beavis and Butt-Head (USA, Europe)', 'File', 'Beavis and Butt-Head (USA, Europe)'], ['Beetlejuice (USA)', 'File', 'Beetlejuice (USA)'], ['Best of the Best - Championship Karate (USA)', 'File', 'Best of the Best - Championship Karate (USA)'], ["Bill & Ted's Excellent Game Boy Adventure - A Bogus Journey! (USA, Europe)", 'File', "Bill & Ted's Excellent Game Boy Adventure - A Bogus Journey! (USA, Europe)"], ["Bill Elliott's NASCAR Fast Tracks (USA)", 'File', "Bill Elliott's NASCAR Fast Tracks (USA)"], ['Bionic Battler (USA)', 'File', 'Bionic Battler (USA)'], ['Bionic Commando (USA)', 'File', 'Bionic Commando (USA)'], ['Black Bass - Lure Fishing (USA)', 'File', 'Black Bass - Lure Fishing (USA)'], ['Blades of Steel (USA)', 'File', 'Blades of Steel (USA)'], ['Blaster Master Boy (USA)', 'File', 'Blaster Master Boy (USA)'], ['Blues Brothers, The (USA, Europe)', 'File', 'Blues Brothers, The (USA, Europe)'], ['Bo Jackson - Two Games in One (USA)', 'File', 'Bo Jackson - Two Games in One (USA)'], ['Boggle Plus (USA)', 'File', 'Boggle Plus (USA)'], ['Bomberman GB (USA, Europe) (SGB Enhanced)', 'File', 'Bomberman GB (USA, Europe) (SGB Enhanced)'], ["Bonk's Adventure (USA)", 'File', "Bonk's Adventure (USA)"], ["Bonk's Revenge (USA) (SGB Enhanced)", 'File', "Bonk's Revenge (USA) (SGB Enhanced)"]]

        if not os.path.exists(roms_directory_path.get()):
            previewConsolesItemList = [['Game Boy', 'Directory', 'Game Boy'], ['Game Boy Advance', 'Directory', 'Game Boy Advance'], ['Game Boy Color', 'Directory', 'Game Boy Color'], ['game-boy-romset-ultra-us', 'Directory', 'game-boy-romset-ultra-us'], ['Nintendo 64', 'Directory', 'Nintendo 64'], ['Nintendo DS', 'Directory', 'Nintendo DS'], ['Nintendo Entertainment System', 'Directory', 'Nintendo Entertainment System'], ['PICO-8', 'Directory', 'PICO-8'], ['Ports', 'Directory', 'Ports'], ['SEGA Mega Drive', 'Directory', 'SEGA Mega Drive'], ['Super Nintendo Entertainment System', 'Directory', 'Super Nintendo Entertainment System']]
        else:
            previewConsolesItemList = list_directory_contents(roms_directory_path.get())
            FolderName = os.path.basename(roms_directory_path.get())

            if os.path.exists(os.path.join(roms_directory_path.get(),previewConsolesItemList[0][0])):
                previewGameItemList = list_directory_contents(os.path.join(roms_directory_path.get(),previewConsolesItemList[0][0]))
                gameFolderName = os.path.basename(os.path.join(roms_directory_path.get(),previewConsolesItemList[0][0]))
            else:
                previewGameItemList = [['4-in-1 Fun Pak [Version 1] (USA, Europe)', 'File', '4-in-1 Fun Pak [Version 1] (USA, Europe)'], ['4-in-1 Funpak - Volume II (USA, Europe)', 'File', '4-in-1 Funpak - Volume II (USA, Europe)'], ['A-mazing Tater (USA)', 'File', 'A-mazing Tater (USA)'], ['Addams Family, The (USA)', 'File', 'Addams Family, The (USA)'], ["Addams Family, The - Pugsley's Scavenger Hunt (USA, Europe) [Revision]", 'File', "Addams Family, The - Pugsley's Scavenger Hunt (USA, Europe) [Revision]"], ['Adventure Island (USA, Europe)', 'File', 'Adventure Island (USA, Europe)'], ['Adventure Island II - Aliens in Paradise (USA, Europe)', 'File', 'Adventure Island II - Aliens in Paradise (USA, Europe)'], ['Adventures of Rocky and Bullwinkle and Friends, The (USA)', 'File', 'Adventures of Rocky and Bullwinkle and Friends, The (USA)'], ['Adventures of Star Saver, The (USA, Europe)', 'File', 'Adventures of Star Saver, The (USA, Europe)'], ['Aerostar (USA, Europe)', 'File', 'Aerostar (USA, Europe)'], ['Aladdin (USA) (SGB Enhanced)', 'File', 'Aladdin (USA) (SGB Enhanced)'], ['Alfred Chicken (USA)', 'File', 'Alfred Chicken (USA)'], ['Alien 3 (USA, Europe)', 'File', 'Alien 3 (USA, Europe)'], ['Alien vs Predator - The Last of His Clan (USA)', 'File', 'Alien vs Predator - The Last of His Clan (USA)'], ['All-Star Baseball 99 (USA)', 'File', 'All-Star Baseball 99 (USA)'], ['Altered Space - A 3-D Alien Adventure (USA)', 'File', 'Altered Space - A 3-D Alien Adventure (USA)'], ['Amazing Penguin (USA, Europe)', 'File', 'Amazing Penguin (USA, Europe)'], ['Amazing Spider-Man, The (USA, Europe)', 'File', 'Amazing Spider-Man, The (USA, Europe)'], ['Animaniacs (USA) (SGB Enhanced)', 'File', 'Animaniacs (USA) (SGB Enhanced)'], ['Arcade Classic No. 1 - Asteroids & Missile Command (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 1 - Asteroids & Missile Command (USA, Europe) (SGB Enhanced)'], ['Arcade Classic No. 2 - Centipede & Millipede (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 2 - Centipede & Millipede (USA, Europe) (SGB Enhanced)'], ['Arcade Classic No. 3 - Galaga & Galaxian (USA) (SGB Enhanced)', 'File', 'Arcade Classic No. 3 - Galaga & Galaxian (USA) (SGB Enhanced)'], ['Arcade Classic No. 4 - Defender & Joust (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classic No. 4 - Defender & Joust (USA, Europe) (SGB Enhanced)'], ['Arcade Classics - Super Breakout & Battlezone (USA, Europe) (SGB Enhanced)', 'File', 'Arcade Classics - Super Breakout & Battlezone (USA, Europe) (SGB Enhanced)'], ['Asteroids (USA, Europe)', 'File', 'Asteroids (USA, Europe)'], ['Atomic Punk (USA)', 'File', 'Atomic Punk (USA)'], ['Attack of the Killer Tomatoes (USA, Europe)', 'File', 'Attack of the Killer Tomatoes (USA, Europe)'], ['Avenging Spirit (USA, Europe)', 'File', 'Avenging Spirit (USA, Europe)'], ['Balloon Kid (USA, Europe)', 'File', 'Balloon Kid (USA, Europe)'], ['Barbie - Game Girl (USA, Europe)', 'File', 'Barbie - Game Girl (USA, Europe)'], ["Bart Simpson's Escape from Camp Deadly (USA, Europe)", 'File', "Bart Simpson's Escape from Camp Deadly (USA, Europe)"], ['Bases Loaded for Game Boy (USA)', 'File', 'Bases Loaded for Game Boy (USA)'], ['Batman - Return of the Joker (USA, Europe)', 'File', 'Batman - Return of the Joker (USA, Europe)'], ['Batman - The Animated Series (USA, Europe)', 'File', 'Batman - The Animated Series (USA, Europe)'], ['Batman Forever (USA, Europe)', 'File', 'Batman Forever (USA, Europe)'], ['Battle Arena Toshinden (USA) (SGB Enhanced)', 'File', 'Battle Arena Toshinden (USA) (SGB Enhanced)'], ['Battle Bull (USA)', 'File', 'Battle Bull (USA)'], ['Battle Unit Zeoth (USA, Europe)', 'File', 'Battle Unit Zeoth (USA, Europe)'], ['Battleship (USA, Europe)', 'File', 'Battleship (USA, Europe)'], ['Battletoads (USA, Europe)', 'File', 'Battletoads (USA, Europe)'], ["Battletoads in Ragnarok's World (USA)", 'File', "Battletoads in Ragnarok's World (USA)"], ['Battletoads-Double Dragon (USA)', 'File', 'Battletoads-Double Dragon (USA)'], ['Beavis and Butt-Head (USA, Europe)', 'File', 'Beavis and Butt-Head (USA, Europe)'], ['Beetlejuice (USA)', 'File', 'Beetlejuice (USA)'], ['Best of the Best - Championship Karate (USA)', 'File', 'Best of the Best - Championship Karate (USA)'], ["Bill & Ted's Excellent Game Boy Adventure - A Bogus Journey! (USA, Europe)", 'File', "Bill & Ted's Excellent Game Boy Adventure - A Bogus Journey! (USA, Europe)"], ["Bill Elliott's NASCAR Fast Tracks (USA)", 'File', "Bill Elliott's NASCAR Fast Tracks (USA)"], ['Bionic Battler (USA)', 'File', 'Bionic Battler (USA)'], ['Bionic Commando (USA)', 'File', 'Bionic Commando (USA)'], ['Black Bass - Lure Fishing (USA)', 'File', 'Black Bass - Lure Fishing (USA)'], ['Blades of Steel (USA)', 'File', 'Blades of Steel (USA)'], ['Blaster Master Boy (USA)', 'File', 'Blaster Master Boy (USA)'], ['Blues Brothers, The (USA, Europe)', 'File', 'Blues Brothers, The (USA, Europe)'], ['Bo Jackson - Two Games in One (USA)', 'File', 'Bo Jackson - Two Games in One (USA)'], ['Boggle Plus (USA)', 'File', 'Boggle Plus (USA)'], ['Bomberman GB (USA, Europe) (SGB Enhanced)', 'File', 'Bomberman GB (USA, Europe) (SGB Enhanced)'], ["Bonk's Adventure (USA)", 'File', "Bonk's Adventure (USA)"], ["Bonk's Revenge (USA) (SGB Enhanced)", 'File', "Bonk's Revenge (USA) (SGB Enhanced)"]]

        if main_menu_style_var.get() == "Horizontal":
            image1 = generatePilImageHorizontal(fakeprogressbar,
                                                0,
                                                bgHexVar.get(),
                                                selectedFontHexVar.get(),
                                                deselectedFontHexVar.get(),
                                                bubbleHexVar.get(),
                                                iconHexVar.get(),
                                                previewRenderFactor,
                                                transparent=False).resize(preview_size, Image.LANCZOS)
        elif main_menu_style_var.get() == "Alt-Horizontal":
            image1 = generatePilImageAltHorizontal(fakeprogressbar,
                                                0,
                                                bgHexVar.get(),
                                                selectedFontHexVar.get(),
                                                deselectedFontHexVar.get(),
                                                bubbleHexVar.get(),
                                                iconHexVar.get(),
                                                previewRenderFactor,
                                                transparent=False).resize(preview_size, Image.LANCZOS)
        elif main_menu_style_var.get() == "Vertical":
            if not page_by_page_var.get():
                image1 = generatePilImageVertical(fakeprogressbar,0,
                                                "muxlaunch",
                                                previewItemList[0:int(items_per_screen_entry.get())],
                                                additions_Blank,
                                                int(textPaddingVar.get()),
                                                int(bubblePaddingVar.get()),
                                                int(items_per_screen_entry.get()),
                                                bgHexVar.get(),
                                                selectedFontHexVar.get(),
                                                deselectedFontHexVar.get(),
                                                bubbleHexVar.get()
                                                ,previewRenderFactor,transparent=False).resize(preview_size, Image.LANCZOS)
            else:
                image1 = generatePilImageVertical(fakeprogressbar,0,
                                "muxlaunch",
                                previewItemList[0:int(items_per_screen_entry.get())],
                                additions_Blank,
                                int(textPaddingVar.get()),
                                int(bubblePaddingVar.get()),
                                int(items_per_screen_entry.get()),
                                bgHexVar.get(),
                                selectedFontHexVar.get(),
                                deselectedFontHexVar.get(),
                                bubbleHexVar.get()
                                ,previewRenderFactor,
                                scrollBarWidth=int(scrollBarWidthVar.get()),
                                showScrollBar=(len(previewItemList)/int(items_per_screen_entry.get()))>1,
                                numScreens=math.ceil(len(previewItemList)/int(items_per_screen_entry.get())),
                                screenIndex=0,transparent=False).resize(preview_size, Image.LANCZOS)
        if not page_by_page_var.get():
            image2 = generatePilImageVertical(fakeprogressbar,0,
                                            "Folder",
                                            previewConsolesItemList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            fileCounter="1 / " + items_per_screen_entry.get(),
                                            transparent=False).resize(preview_size, Image.LANCZOS)
            image3 = generatePilImageVertical(fakeprogressbar,0,
                                            consoleName, 
                                            previewGameItemList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            fileCounter="1 / " + items_per_screen_entry.get(),
                                            folderName=gameFolderName,
                                            transparent=False).resize(preview_size, Image.LANCZOS)
            image4 = generatePilImageVertical(fakeprogressbar,0,
                                            "muxapp",
                                            previewApplicationList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            fileCounter="1 / " + items_per_screen_entry.get(),
                                            transparent=False).resize(preview_size, Image.LANCZOS)
        else:
            image2 = generatePilImageVertical(fakeprogressbar,0,
                                            "Folder",
                                            previewConsolesItemList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            scrollBarWidth=int(scrollBarWidthVar.get()),
                                            showScrollBar=(len(previewConsolesItemList)/int(items_per_screen_entry.get()))>1,
                                            numScreens=math.ceil(len(previewConsolesItemList)/int(items_per_screen_entry.get())),
                                            screenIndex=0,
                                            fileCounter="1 / " + items_per_screen_entry.get(),
                                            transparent=False).resize(preview_size, Image.LANCZOS)
            image3 = generatePilImageVertical(fakeprogressbar,0,
                                            consoleName,
                                            previewGameItemList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            scrollBarWidth=int(scrollBarWidthVar.get()),
                                            showScrollBar=(len(previewGameItemList)/int(items_per_screen_entry.get()))>1,
                                            numScreens=math.ceil(len(previewGameItemList)/int(items_per_screen_entry.get())),
                                            screenIndex=0,
                                            fileCounter="1 / " + items_per_screen_entry.get(),
                                            transparent=False).resize(preview_size, Image.LANCZOS)
            image4 = generatePilImageVertical(fakeprogressbar,0,
                                            "muxapp",
                                            previewApplicationList[0:int(items_per_screen_entry.get())],
                                            additions_Blank,
                                            int(textPaddingVar.get()),
                                            int(bubblePaddingVar.get()),
                                            int(items_per_screen_entry.get()),
                                            bgHexVar.get(),
                                            selectedFontHexVar.get(),
                                            deselectedFontHexVar.get(),
                                            bubbleHexVar.get(),
                                            previewRenderFactor,
                                            scrollBarWidth=int(scrollBarWidthVar.get()),
                                            showScrollBar=(len(previewApplicationList)/int(items_per_screen_entry.get()))>1,
                                            numScreens=math.ceil(len(previewApplicationList)/int(items_per_screen_entry.get())),
                                            screenIndex=0,fileCounter="1 / " + items_per_screen_entry.get(),
                                            transparent=False).resize(preview_size, Image.LANCZOS)
        if main_menu_style_var.get() == "Horizontal":
            image5 = generatePilImageHorizontal(fakeprogressbar,
                                                4,
                                                bgHexVar.get(),
                                                selectedFontHexVar.get(),
                                                deselectedFontHexVar.get(),
                                                bubbleHexVar.get(),
                                                iconHexVar.get(),
                                                previewRenderFactor,
                                                transparent=False).resize(preview_size, Image.LANCZOS)
        
        elif main_menu_style_var.get() == "Alt-Horizontal":
            image5 = generatePilImageAltHorizontal(fakeprogressbar,
                                                4,
                                                bgHexVar.get(),
                                                selectedFontHexVar.get(),
                                                deselectedFontHexVar.get(),
                                                bubbleHexVar.get(),
                                                iconHexVar.get(),
                                                previewRenderFactor,
                                                transparent=False).resize(preview_size, Image.LANCZOS)

        if include_overlay_var.get() and selected_overlay_var.get() != "":
            preview_overlay_resized = preview_overlay_image.resize(image1.size, Image.LANCZOS)
            image1.paste(preview_overlay_resized,(0,0),preview_overlay_resized)
            image2.paste(preview_overlay_resized,(0,0),preview_overlay_resized)
            image3.paste(preview_overlay_resized,(0,0),preview_overlay_resized)
            image4.paste(preview_overlay_resized,(0,0),preview_overlay_resized)
            if main_menu_style_var.get() != "Vertical":
                image5.paste(preview_overlay_resized,(0,0),preview_overlay_resized)
    
        update_image_label(image_label1, image1)
        update_image_label(image_label2, image2)
        update_image_label(image_label3, image3)
        update_image_label(image_label4, image4)
        if main_menu_style_var.get() != "Vertical":
            update_image_label(image_label5, image5)
        else:
            remove_image_from_label(image_label5)
        valid_params = True
    except:
        if get_current_image(image_label1) != None and get_current_image(image_label2) != None and get_current_image(image_label3) != None and get_current_image(image_label4) != None and get_current_image(image_label5) != None:
            if valid_params:
                redOutlineImage1 = outline_image_with_inner_gap(get_current_image(image_label1)).resize(preview_size, Image.LANCZOS)
                redOutlineImage2 = outline_image_with_inner_gap(get_current_image(image_label2)).resize(preview_size, Image.LANCZOS)
                redOutlineImage3 = outline_image_with_inner_gap(get_current_image(image_label3)).resize(preview_size, Image.LANCZOS)
                redOutlineImage4 = outline_image_with_inner_gap(get_current_image(image_label4)).resize(preview_size, Image.LANCZOS)
                if main_menu_style_var.get() != "Vertical":
                    redOutlineImage5 = outline_image_with_inner_gap(get_current_image(image_label5)).resize(preview_size, Image.LANCZOS)
                update_image_label(image_label1, redOutlineImage1)
                update_image_label(image_label2, redOutlineImage2)
                update_image_label(image_label3, redOutlineImage3)
                update_image_label(image_label4, redOutlineImage4)
                if main_menu_style_var.get() != "Vertical":
                    update_image_label(image_label5, redOutlineImage5)
                valid_params = False


def save_settings():
    config.scrollBarWidthVar = scrollBarWidthVar.get()
    config.textPaddingVar = textPaddingVar.get()
    config.bubblePaddingVar = bubblePaddingVar.get()
    config.itemsPerScreenVar = itemsPerScreenVar.get()
    config.footerHeightVar = footerHeightVar.get()
    config.customFontSizeVar = customFontSizeVar.get()
    config.bgHexVar = bgHexVar.get()
    config.selectedFontHexVar = selectedFontHexVar.get()
    config.deselectedFontHexVar = deselectedFontHexVar.get()
    config.bubbleHexVar = bubbleHexVar.get()
    config.iconHexVar = iconHexVar.get()
    config.remove_brackets_var = remove_brackets_var.get()
    config.remove_square_brackets_var = remove_square_brackets_var.get()
    config.replace_hyphen_var = replace_hyphen_var.get()
    config.also_games_var = also_games_var.get()
    config.move_the_var = move_the_var.get()
    config.include_overlay_var = include_overlay_var.get()
    config.alternate_menu_names_var = alternate_menu_names_var.get()
    config.remove_right_menu_guides_var = remove_right_menu_guides_var.get()
    config.remove_left_menu_guides_var = remove_left_menu_guides_var.get()
    config.overlay_box_art_var = overlay_box_art_var.get()
    config.box_art_directory_path = box_art_directory_path.get()
    config.maxGamesBubbleLengthVar = maxGamesBubbleLengthVar.get()
    config.maxFoldersBubbleLengthVar = maxFoldersBubbleLengthVar.get()
    config.roms_directory_path = roms_directory_path.get()
    config.application_directory_path = application_directory_path.get()
    config.previewConsoleNameVar = previewConsoleNameVar.get()
    config.show_hidden_files_var = show_hidden_files_var.get()
    config.override_bubble_cut_var = override_bubble_cut_var.get()
    config.page_by_page_var = page_by_page_var.get()
    config.transparent_text_var = transparent_text_var.get()
    config.override_font_size_var = override_font_size_var.get()
    config.legacy_generation_var = legacy_generation_var.get()
    config.override_folder_box_art_padding_var = override_folder_box_art_padding_var.get()
    config.boxArtPaddingVar = boxArtPaddingVar.get()
    config.folderBoxArtPaddingVar = folderBoxArtPaddingVar.get()
    config.content_alignment_var = content_alignment_var.get()
    config.theme_alignment_var = theme_alignment_var.get()
    config.main_menu_style_var = main_menu_style_var.get()
    config.version_var = version_var.get()
    config.global_alignment_var = global_alignment_var.get()
    config.selected_overlay_var = selected_overlay_var.get()
    config.am_theme_directory_path = am_theme_directory_path.get()
    config.theme_directory_path = theme_directory_path.get()
    config.catalogue_directory_path = catalogue_directory_path.get()
    config.name_json_path = name_json_path.get()
    config.background_image_path = background_image_path.get()
    config.bootlogo_image_path = bootlogo_image_path.get()
    config.alt_font_path = alt_font_path.get()
    config.alt_text_path = alt_text_path.get()
    config.use_alt_font_var = use_alt_font_var.get()
    config.use_custom_bootlogo_var = use_custom_bootlogo_var.get()
    config.rg28xxVar = rg28xxVar.get()
    config.themeName = theme_name_entry.get()
    config.amThemeName = am_theme_name_entry.get()
    config.am_ignore_theme_var = am_ignore_theme_var.get()
    config.am_ignore_cd_var = am_ignore_cd_var.get()
    config.advanced_error_var = advanced_error_var.get()
    config.show_file_counter_var = show_file_counter_var.get()
    config.show_console_name_var = show_console_name_var.get()

def load_settings():
    scrollBarWidthVar.set(config.scrollBarWidthVar)
    textPaddingVar.set(config.textPaddingVar)
    bubblePaddingVar.set(config.bubblePaddingVar)
    itemsPerScreenVar.set(config.itemsPerScreenVar)
    footerHeightVar.set(config.footerHeightVar)
    boxArtPaddingVar.set(config.boxArtPaddingVar)
    folderBoxArtPaddingVar.set(config.folderBoxArtPaddingVar)
    customFontSizeVar.set(config.customFontSizeVar)
    bgHexVar.set(config.bgHexVar)
    selectedFontHexVar.set(config.selectedFontHexVar)
    deselectedFontHexVar.set(config.deselectedFontHexVar)
    bubbleHexVar.set(config.bubbleHexVar)
    iconHexVar.set(config.iconHexVar)
    remove_brackets_var.set(config.remove_brackets_var)
    remove_square_brackets_var.set(config.remove_square_brackets_var)
    replace_hyphen_var.set(config.replace_hyphen_var)
    also_games_var.set(config.also_games_var)
    move_the_var.set(config.move_the_var)
    include_overlay_var.set(config.include_overlay_var)
    alternate_menu_names_var.set(config.alternate_menu_names_var)
    remove_right_menu_guides_var.set(config.remove_right_menu_guides_var)
    remove_left_menu_guides_var.set(config.remove_left_menu_guides_var)
    overlay_box_art_var.set(config.overlay_box_art_var)
    box_art_directory_path.set(config.box_art_directory_path)
    maxGamesBubbleLengthVar.set(config.maxGamesBubbleLengthVar)
    maxFoldersBubbleLengthVar.set(config.maxFoldersBubbleLengthVar)
    roms_directory_path.set(config.roms_directory_path)
    application_directory_path.set(config.application_directory_path)
    previewConsoleNameVar.set(config.previewConsoleNameVar)
    show_hidden_files_var.set(config.show_hidden_files_var)
    override_bubble_cut_var.set(config.override_bubble_cut_var)
    override_folder_box_art_padding_var.set(config.override_folder_box_art_padding_var)
    page_by_page_var.set(config.page_by_page_var)
    transparent_text_var.set(config.transparent_text_var)
    override_font_size_var.set(config.override_font_size_var)
    legacy_generation_var.set(config.legacy_generation_var)
    version_var.set(config.version_var)
    global_alignment_var.set(config.global_alignment_var)
    selected_overlay_var.set(config.selected_overlay_var)
    theme_alignment_var.set(config.theme_alignment_var)
    main_menu_style_var.set(config.main_menu_style_var)
    content_alignment_var.set(config.content_alignment_var)
    am_theme_directory_path.set(config.am_theme_directory_path)
    theme_directory_path.set(config.theme_directory_path)
    catalogue_directory_path.set(config.catalogue_directory_path)
    name_json_path.set(config.name_json_path)
    background_image_path.set(config.background_image_path)
    bootlogo_image_path.set(config.bootlogo_image_path)
    alt_font_path.set(config.alt_font_path)
    alt_text_path.set(config.alt_text_path)
    use_alt_font_var.set(config.use_alt_font_var)
    use_custom_bootlogo_var.set(config.use_custom_bootlogo_var)
    rg28xxVar.set(config.rg28xxVar)
    theme_name_entry.delete(0, tk.END)
    theme_name_entry.insert(0, config.themeName)
    am_theme_name_entry.delete(0, tk.END)
    am_theme_name_entry.insert(0, config.amThemeName)
    am_ignore_theme_var.set(config.am_ignore_theme_var)
    am_ignore_cd_var.set(config.am_ignore_cd_var)
    advanced_error_var.set(config.advanced_error_var)
    show_file_counter_var.set(config.show_file_counter_var)
    show_console_name_var.set(config.show_console_name_var)


config = Config()
load_settings()
consoleMap = getConsoleAssociationList()
menuNameMap = getAlternateMenuNameDict()

# Attach trace callbacks to the variables
scrollBarWidthVar.trace_add("write", on_change)
textPaddingVar.trace_add("write", on_change)
bubblePaddingVar.trace_add("write", on_change)
itemsPerScreenVar.trace_add("write", on_change)
footerHeightVar.trace_add("write", on_change)
boxArtPaddingVar.trace_add("write", on_change)
folderBoxArtPaddingVar.trace_add("write", on_change)
customFontSizeVar.trace_add("write", on_change)
bgHexVar.trace_add("write", on_change)
selectedFontHexVar.trace_add("write", on_change)
deselectedFontHexVar.trace_add("write", on_change)
bubbleHexVar.trace_add("write", on_change)
iconHexVar.trace_add("write", on_change)
remove_brackets_var.trace_add("write", on_change)
remove_square_brackets_var.trace_add("write", on_change)
replace_hyphen_var.trace_add("write", on_change)
also_games_var.trace_add("write", on_change)
show_file_counter_var.trace_add("write", on_change)
show_console_name_var.trace_add("write", on_change)
move_the_var.trace_add("write", on_change)
include_overlay_var.trace_add("write", on_change)
alternate_menu_names_var.trace_add("write", on_change)
remove_right_menu_guides_var.trace_add("write", on_change)
remove_left_menu_guides_var.trace_add("write", on_change)
overlay_box_art_var.trace_add("write", on_change)
box_art_directory_path.trace_add("write", on_change)
maxGamesBubbleLengthVar.trace_add("write", on_change)
maxFoldersBubbleLengthVar.trace_add("write", on_change)
roms_directory_path.trace_add("write", on_change)
application_directory_path.trace_add("write", on_change)
previewConsoleNameVar.trace_add("write", on_change)
show_hidden_files_var.trace_add("write", on_change)
override_bubble_cut_var.trace_add("write", on_change)
override_folder_box_art_padding_var.trace_add("write", on_change)
page_by_page_var.trace_add("write", on_change)
transparent_text_var.trace_add("write", on_change)
override_font_size_var.trace_add("write", on_change)
legacy_generation_var.trace_add("write",on_change)
version_var.trace_add("write", on_change)
global_alignment_var.trace_add("write", on_change)
selected_overlay_var.trace_add("write",on_change)
content_alignment_var.trace_add("write", on_change)
theme_alignment_var.trace_add("write", on_change)
main_menu_style_var.trace_add("write",on_change)
am_theme_directory_path.trace_add("write", on_change)
theme_directory_path.trace_add("write", on_change)
catalogue_directory_path.trace_add("write", on_change)
name_json_path.trace_add("write", on_change)
background_image_path.trace_add("write", on_change)
bootlogo_image_path.trace_add("write", on_change)
am_ignore_theme_var.trace_add("write", on_change)
am_ignore_cd_var.trace_add("write", on_change)
advanced_error_var.trace_add("write", on_change)
use_alt_font_var.trace_add("write", on_change)
use_custom_bootlogo_var.trace_add("write", on_change)
rg28xxVar.trace_add("write",on_change)
alt_font_path.trace_add("write", on_change)
alt_text_path.trace_add("write",on_change)



on_change()

# Run the main loop
root.mainloop()