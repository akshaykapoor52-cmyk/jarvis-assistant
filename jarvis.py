import datetime
import os
import webbrowser
import pyttsx3
import speech_recognition as sr

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
  print(f'JARVIS: {text}')
  engine.say(text)
  engine.runAndWait()


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
  with sr.Microphone() as source:
    print('Listening...')
    r.pause_threshold = 1
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

  try:
    print('Recognizing...')
    query = r.recognize_google(audio, language='en-US')
    print(f'User said: {query}\n')
  except Exception as e:
    print('Say that again please...')
    return 'None'
  return query.lower()


if __name__ == '__main__':
  wish_user()

  while True:
    query = take_command()

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