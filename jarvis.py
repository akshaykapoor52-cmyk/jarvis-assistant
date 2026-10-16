import datetime
import os
import sys
import webbrowser
import pyttsx3
import speech_recognition as sr

# Fix standard output streams when running --noconsole mode
if sys.stdout is None:
  sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
  sys.stderr = open(os.devnull, 'w')


def speak(text):
  print(f'JARVIS: {text}')
  try:
    # Re-initialize engine locally inside speak to prevent Windows engine lock
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 170)  # Moderate speaking rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
  except Exception as e:
    print(f'Speech Error: {e}')


def wish_user():
  hour = int(datetime.datetime.now().hour)
  if hour >= 0 and hour < 12:
    speak('Good Morning, Sir.')
  elif hour >= 12 and hour < 18:
    speak('Good Afternoon, Sir.')
  else:
    speak('Good Evening, Sir.')
  speak('JARVIS is online and ready. How can I help you?')


def take_command():
  r = sr.Recognizer()
  # Adjust recognition sensitivity
  r.energy_threshold = 300
  r.dynamic_energy_threshold = True

  with sr.Microphone() as source:
    print('Listening...')
    r.pause_threshold = 1
    r.adjust_for_ambient_noise(source, duration=1)
    try:
      audio = r.listen(source, timeout=5, phrase_time_limit=8)
    except sr.WaitTimeoutError:
      return 'none'

  try:
    print('Recognizing...')
    query = r.recognize_google(audio, language='en-US')
    print(f'User said: {query}\n')
  except sr.UnknownValueError:
    return 'none'
  except Exception as e:
    print(f'Error recognizing speech: {e}')
    return 'none'

  return query.lower()


if __name__ == '__main__':
  wish_user()

  while True:
    query = take_command()

    if query == 'none':
      continue

    if 'open google' in query:
      speak('Opening Google, Sir.')
      webbrowser.open('https://google.com')

    elif 'open youtube' in query:
      speak('Opening YouTube.')
      webbrowser.open('https://youtube.com')

    elif 'the time' in query:
      str_time = datetime.datetime.now().strftime('%H:%M:%S')
      speak(f'Sir, the current time is {str_time}')

    elif 'search for' in query:
      speak('Searching the web.')
      search_term = query.replace('search for', '')
      webbrowser.open(f'https://www.google.com/search?q={search_term}')

    elif 'exit' in query or 'offline' in query:
      speak('Going offline, Sir. Have a great day.')
      break
