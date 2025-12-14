import requests
import time
import logging

import mesop as me
from dataclasses import field
import json


@me.stateclass
class State:
  input: str
  output: str
  history: list[str] = field(default_factory=lambda: [])
  in_progress: bool


@me.page(path="/")
def page():
  with me.box(
    style=me.Style(
      background="#fff",
      min_height="calc(100% - 48px)",
      padding=me.Padding(bottom=16),
    )
  ):
    with me.box(
      style=me.Style(
        width="min(720px, 100%)",
        margin=me.Margin.symmetric(horizontal="auto"),
        padding=me.Padding.symmetric(
          horizontal=16,
        ),
      )
    ):
      header_text()
      chat_input()
      output()
  footer()


def header_text():
  with me.box(
    style=me.Style(
      padding=me.Padding(
        top=64,
        bottom=36,
      ),
    )
  ):
    me.text(
      "Dongtt ChatPT",
      style=me.Style(
        font_size=36,
        font_weight=700,
        background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
        color="transparent",
      ),
    )

def chat_input():
  state = me.state(State)
  with me.box(
    style=me.Style(
      padding=me.Padding.all(8),
      background="white",
      display="flex",
      width="100%",
      border=me.Border.all(
        me.BorderSide(width=1, style="solid", color="#DDD")
      ),
      border_radius=16,
      box_shadow="0 4px 12px #00000010",
    )
  ):
    with me.box(
      style=me.Style(
        flex_grow=1,
      )
    ):
      me.native_textarea(
        value=state.input,
        autosize=True,
        min_rows=4,
        placeholder="Enter your prompt",
        style=me.Style(
          padding=me.Padding(top=16, left=16),
          background="white",
          outline="none",
          width="100%",
          overflow_y="auto",
          border=me.Border.all(
            me.BorderSide(style="none"),
          ),
        ),
        on_blur=textarea_on_blur,
      )
    with me.content_button(type="icon", on_click=click_send):
      me.icon("send")

def textarea_on_blur(e: me.InputBlurEvent):
  state = me.state(State)
  state.input = e.value

def click_send(e: me.ClickEvent):
  state = me.state(State)
  if not state.input:
    return

  user_input = state.input
  state.input = ""

  state.history.append(["user", user_input])
  state.in_progress = True
  yield
  history_to_send = state.history[:-1]
  response = call_api(user_input, history_to_send);
  for reply in response:
    if reply and (not state.history or state.history[-1][0] != "assistant"):
      state.history.append(["assistant", reply])
    yield

  state.in_progress = False
  yield

def call_api(user_input, history):
  url = "http://127.0.0.1:9696/chat"
  payload = {
    "message": user_input,
    "history": history
  }
  logging.info("Sending request payload: %s", payload)
  try:
    resp = requests.post(url, json=payload)
    logging.info("response=%s", resp.json())

    if resp.status_code != 200:
      yield f"Error: Received status code {resp.status_code}", history
      return

    data = resp.json()
    reply = data.get("reply", "")
    yield reply
  except Exception as e:
    yield f"Error: {e}", history

def output():
  state = me.state(State)
  if state.history or state.in_progress:
    with me.box(
      style=me.Style(
        background="#F0F4F9",
        padding=me.Padding.all(16),
        border_radius=16,
        margin=me.Margin(top=36),
        font_size=14,
        overflow_y="auto",
        max_height="60vh",
        display="flex",
        flex_direction="column",
        gap="8px",
      ),
      key="chat_container"
    ) as container:
      for idx, item in enumerate(state.history):
        role, text = item
        align_style = me.Style(
          display="flex",
          justify_content="flex-end" if role == "user" else "flex-start"
        )
        bubble_style = me.Style(
          padding=me.Padding.all(12),
          border_radius=12,
          max_width="90%",
          background="#DCF8C6" if role == "user" else "#FFFFFF",
          color="#000000",
          white_space="pre-wrap",
          box_shadow="0 1px 3px #0000001a",
        )
        msg_key = f"msg_{idx}"
        with me.box(style=align_style):
          me.markdown(text, style=bubble_style, key=msg_key)

      if state.in_progress:
        with me.box(style=me.Style(margin=me.Margin(top=16))):
          me.progress_spinner()

      last_msg_key = f"msg_{len(state.history)-1}"
      me.scroll_into_view(key=last_msg_key)

def footer():
  with me.box(
    style=me.Style(
      position="sticky",
      bottom=0,
      padding=me.Padding.symmetric(vertical=16, horizontal=16),
      width="100%",
      background="#F0F4F9",
      font_size=14,
    )
  ):
    me.html(
      "Made with <a href='#'>Dongttfd ChatPT</a>",
    )
