#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:08:38 2021

@author: Eric Gitonga
"""
import streamlit as st
import streamlit_analytics
import cv2
import numpy as np
from PIL import Image

icon = Image.open("images/fly.jpg")

st.set_page_config(
    page_title="Super Basic Photo Editor",
    page_icon=icon,
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Super Basic Photo Editor")

