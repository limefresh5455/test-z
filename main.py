import threading
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import pandas as pd
import speech_recognition as sr
import moviepy.editor as mp
import os
import PyPDF2
from pytube import YouTube
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import tempfile
from moviepy.editor import VideoFileClip
import urllib.parse
from typing import List
import concurrent.futures
import time
import difflib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(title="FastAPI APP Endpoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items")
async def read_item():
    return {"item_id": "WORKING"}
