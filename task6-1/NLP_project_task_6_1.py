# -*- coding: utf-8 -*-
"""task61.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1du09Sw5eFbCXPfDkHBNfJf0hkzaVM7tV

# ***Projekt INL - 1. Wykrywanie cyberprzemocy***
Wykonali: Tomasz Smyczyński s23689, Michał Niski s23096

# Task 6-1

Zadanie polega na rozpoznaniu pomiędzy tweetami, które są normalne/nieszkodliwe (label 0) oraz tweetami, które zawierają jakiekolwiek szkodliwe informacje (label 1). Zawiera to w sobie cyberprzemoc, mowę nienawiści oraz podobne zjawiska. Dane do zadania zostały udostępnione w zakładce "Pliki", w folderze "Projekty" na stronie przedmiotu INL.

## Import podstawowych bibliotek oraz obsługa datasetów

Import bibliotek Tensorflow oraz scikit-learn:
"""

import tensorflow as tf
import sklearn
from sklearn.model_selection import train_test_split

""" Deklaracje funkcji importu plików tekstowych: training_set_clean_only_tags.txt oraz training_set_clean_only_text.txt, konwersji zawartości pliku z etykietami oraz podziału zawartości plików na datasety treningowe oraz testowe:"""

def read_file(path, strip=True):
  with open(path, encoding='utf8') as file:
    data = file.readlines()
  if strip: data = [line.strip() for line in data]
  return data


def change_labels_to_negative_positive_boolean_values(labels: list) -> list:
  '''
  Zamierzony efekt:
  [{'CYBERBULLY': True, 'NOTCYBERBULLY': False},
  {'CYBERBULLY': False, 'NOTCYBERBULLY': True},
  itd.
  '''
  values = []
  for label in labels:
    values.append({"CYBERBULLY": bool(int(label)), "NOTCYBERBULLY": not bool(int(label))})
  return values

def load_source_data(test_size):
  '''
  Otwieramy pliki za pomocą wcześniej zadeklarowanej funkcji,
  a następnie dzielimy ich zawartość na zestawy treningowe oraz testowe.
  '''
  training_set_clean_only_tags = []
  training_set_clean_only_text = []
  training_set_clean_only_tags = read_file('training_set_clean_only_tags.txt')
  training_set_clean_only_text = read_file('training_set_clean_only_text.txt')
  splits_one = train_test_split(training_set_clean_only_tags, test_size=test_size, random_state=0)
  splits_two = train_test_split(training_set_clean_only_text, test_size=test_size, random_state=0)
  training_labels, test_labels = splits_one
  training_text, test_text = splits_two
  

  training_labels = change_labels_to_negative_positive_boolean_values(training_labels)
  test_labels = change_labels_to_negative_positive_boolean_values(test_labels)
  print('Textcat format: True')

  return (training_text, training_labels), (test_text, test_labels)

"""## Podejście pierwsze (klasyfikacja/kategoryzacja): dataset treningowy: 80%, dataset testowy: 20%

### Podział datasetów na sety treningowe oraz testowe wraz z wyświetleniem informacji o nich

Wywołanie funkcji importu oraz podział na dataset treningowy oraz testowy ze współczynnikiem testowym 0.2:
"""

(training_text, training_labels), (test_text, test_labels) = load_source_data(0.2)
print((training_text, training_labels), (test_text, test_labels))

"""Pokazanie przykładów datasetu treningowego oraz testowego:

"""

limit = 0

print('\nPrzykłady treningowe:')
for (label, text) in zip(training_labels, training_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

limit = 0

print('\nPrzykłady testowe:')
for (label, text) in zip(test_labels, test_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

"""Wyprintowanie liczby zdań treningowych, liczby zdań testowych oraz sumy wszystkich tekstów:"""

sum_number = len(training_labels + test_labels)
print(f'Liczba zdań treningowych: {len(training_text)} ({round(len(training_text)/sum_number *100, 2)}%).')
print(f'Liczba zdań testowych: {len(test_text)} ({round(len(test_text)/sum_number *100, 2)}%).')
print(f'Suma wszystkich zdań: {sum_number}')

"""Sprawdzanie odsetka komentarzy, które są cyberprzemocą oraz które nią nie są dla setu treningowego oraz treningowego i testowego razem:"""

counter = 0
for label in training_labels:
  if label['CYBERBULLY'] == True:
    counter += 1
print(f'Liczba zdań w secie treningowym, które są cyberprzemocą: {counter} ({round(counter/len(training_labels) *100, 2)}%).')

counter_cyberbully = 0
counter_notcyberbully = 0
for label in training_labels + test_labels:
  if label['CYBERBULLY'] == True:
    counter_cyberbully += 1
  else:
    counter_notcyberbully += 1

if counter_cyberbully + counter_notcyberbully == sum_number:
  print(f'Liczba zdań, które nie są cyberprzemocą w obu setach - treningowym i testowym: {counter_notcyberbully} ({round(counter_notcyberbully/sum_number *100, 2)}%).')
  print(f'Liczba zdań, które są cyberprzemocą w obu setach - treningowym i testowym: {counter_cyberbully} ({round(counter_cyberbully/sum_number *100, 2)}%).')

"""### Obróbka datasetów

Oczyszczanie datasetów z elementów charakterystycznych dla portalu Twitter, w celu posiadania samego zdania (chodzi o oznaczenia anonimowych użytkowników - '@anonymized_account' oraz oznaczenie 'RT' symbolizujące udostępnienie dalej):
"""

def twitter_clean(texts):
  replace = {'@anonymized_account': '','rt': ''}
  cleaned_texts = []
  for text in texts:
    text = text.lower()
    for not_cleaned, cleaned in replace.items():
      text = text.replace(not_cleaned, cleaned)
    cleaned_texts.append(text.strip())
  return cleaned_texts

training_text = twitter_clean(training_text)
print(training_text)

"""Pozbycie się ze zdań tzw. stop words, czyli słów, które są powszechnie używane, a ich analiza nie przynosi żadnych korzyści identyfikacyjnych (w praktyce są to przyimki oraz spójniki):"""

!python3 -m pip install -U stop_words --quiet

from stop_words import get_stop_words

# Przyimki
polish_prepositions = ['z', 'do', 'na', 'bez', 'za', 'pod', 'u', 'w', 'nad', 'o', 'od', 'po']
# Spójniki
polish_conjunctions = ['a', 'i', 'oraz', 'tudzież', 'ale', 'jednak', 'lecz', 'natomiast', 'zaś', 'czyli', 'mianowicie', 'ponieważ', 'dlatego', 'przeto', 'tedy', 'więc', 'zatem', 'toteż']

stop_words = get_stop_words('pl')
stop_words = set(stop_words + polish_prepositions + polish_conjunctions)

"""Surowe dane mogą być zwizualizowane w sposób bardzo atrakcyjny, jednym z przykładów jest tzw. word cloud. Jest to graficzna reprezentacja częstości występowania słów. Im większe jest słowo - tym częściej występuje. Graficzne przedstawienie najpopularniejszych słów dla oczyszczonych danych (workcloud oraz pyplot):"""

# Commented out IPython magic to ensure Python compatibility.
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.pyplot as plt
# %matplotlib inline

def get_most_common(txt, top=20):
  words = (txt).split()
  print(f'Found {len(words)} words.')
  most_common = Counter(words).most_common(top)
  labels = []
  texts = []
  for label, text in most_common:
    labels.append(label)
    texts.append(text)
  return texts, labels

def plot_most_common(txt, top=20, title=''):
  values, labels = get_most_common(txt, top)
  x = range(len(values))

  plt.figure(figsize=(15, 5))
  plt.bar(x, values)
  plt.xticks(x, labels, rotation=90)
  plt.title(title)
  plt.show()

def wordcloud_plot(text: str, stop_words=None, bg='white'):
  wordcloud = WordCloud(stopwords=stop_words,
                        min_font_size=5, #4
                        max_words=150, #200
                        background_color=bg,
                        ).generate(text)
  plt.figure(figsize=(10, 8))
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.plot()

txt_train = ' '.join(training_text)
wordcloud_plot(txt_train, stop_words)
plot_most_common(txt_train, top=20, title='Dwadzieścia najpopularniejszych słów po oczyszczeniu datasetu:')

"""Podział tekstów według kategorii wraz z graficzną interpretacją najpopularniejszych słów dla każdej z kategorii:"""

def category_split(texts, labels, clean=True):
  cyberbully_texts = []
  notcyberbully_texts = []
  cyberbully_texts_counter = 0
  notcyberbully_texts_counter = 0
  for text, label in zip(texts, labels):
    if label['CYBERBULLY'] == True:
      cyberbully_texts.append(text)
      cyberbully_texts_counter += 1
    else:
      notcyberbully_texts.append(text)
      notcyberbully_texts_counter += 1
  print(f'Teksty związane z cyberprzemocą: {cyberbully_texts_counter}')
  print(f'Teksty niezwiązane z cyberprzemocą: {notcyberbully_texts_counter}')
  if clean:
    cyberbully_texts = twitter_clean(cyberbully_texts)
    notcyberbully_texts = twitter_clean(notcyberbully_texts)
  return cyberbully_texts, notcyberbully_texts


cyberbully_texts = []
notcyberbully_texts = []
for texts, labels in ((training_text, training_labels), (test_text, test_labels)):
  cyberbully, notcyberbully = category_split(texts, labels)
  cyberbully_texts += cyberbully
  notcyberbully_texts += notcyberbully

txt_cyberbully = ' '.join(cyberbully_texts)
wordcloud_plot(txt_cyberbully, stop_words, bg='white')
plot_most_common(txt_cyberbully, top=20, title='Dwadzieścia najpopularniejszych słów w zdaniach związanych z cyberprzemocą:')

txt_notcyberbully = ' '.join(notcyberbully_texts)
wordcloud_plot(txt_notcyberbully, stop_words, bg='white')
plot_most_common(txt_notcyberbully, top=20, title='Dwadzieścia najpopularniejszych słów w zdaniach niezwiązanych z cyberprzemocą:')

"""### Dostosowanie etykiet treningowych do dalszej obróbki"""

def train_labels_formatting(training_text: list, training_labels: list) -> list:
  train_data = list(zip(training_text, [{"cats": cats} for cats in training_labels]))
  return train_data

train_data = train_labels_formatting(training_text, training_labels)
train_data[:1]

"""### Instalacja i załadowanie biblioteki SpaCy

W celu tokenizacji, lematyzacji, a następnie przeprowadzenia treningu zdecydowaliśmy się na bibliotekę spaCy ze względu na prostotę obsługi, łatwą obsługę języka polskiego oraz na to, że korzystaliśmy z niej podczas zajęć :)
"""

import os

!sudo apt-get install build-essential python-dev git
!git clone --branch "v2.3.x" https://github.com/explosion/spaCy && \
cd spaCy && \
python3 -m pip install -U pip setuptools wheel --quiet && \
python3 -m pip install .[lookups] --quiet && \
python3 -m pip install -r requirements.txt --quiet

!wget https://github.com/explosion/spacy-models/releases/download/pl_core_news_sm-2.3.0/pl_core_news_sm-2.3.0.tar.gz
!tar -xvf pl_core_news_sm-2.3.0.tar.gz

language_model = os.path.join('pl_core_news_sm-2.3.0', 'pl_core_news_sm', 'pl_core_news_sm-2.3.0')

import spacy
from spacy.lang.pl.stop_words import STOP_WORDS as stop_words_spacy

nlp = spacy.load(language_model)

"""### Tokenizacja i lematyzacja danych treningowych

Na wcześniej opracowanych i odpowiednio przygotowanych danych dokonujemy lematyzacji, czyli sprowadzeniu każdego ze słów do ich podstawowej formy (np. ma -> mieć):
"""

def lemmatize_train_data(texts: list, nlp: spacy) -> list:
  
  def is_redundant(token):
    return any([token.is_punct, token.is_stop, token.is_space])

  return [' '.join([token.lemma_ for token in nlp(text) if not is_redundant(token)]) for text in texts]

training_text_lemmatized = lemmatize_train_data(training_text, nlp)

print(training_text[:1])
print(training_text_lemmatized[:1])

"""Word cloud dla zlematyzowanych tekstów treningowych:"""

txt_training_lemmatized = ' '.join(training_text_lemmatized)
wordcloud_plot(txt_training_lemmatized, stop_words_spacy, 'white')

"""Podgląd przykładowego obraźliwego komentarza przed i po lematyzacji:

"""

cyberbully_texts_lemmatized = lemmatize_train_data(cyberbully_texts, nlp)
print(cyberbully_texts[:1])
print(cyberbully_texts_lemmatized[:1])

"""Graficzne przedstawienie najbardziej popularnych słów w grupie tweetów związanych z cyberprzemocą:"""

txt_bully_lemmatized = ' '.join(cyberbully_texts_lemmatized)
wordcloud_plot(txt_bully_lemmatized, stop_words_spacy, bg='white')
plot_most_common(txt_bully_lemmatized)

"""### Trening

Trening ze względu na długi czas wykonania jednej epochi będzie wykonany tylko dla 5 epoch. Im większa jest ta wartość, tym wyniki osiągane przez nas będą bardziej zadowalające.
"""

def evaluate_texts(tokenizer, textcat, texts, cats):
  docs = (tokenizer(text) for text in texts)
  tp = 0.0  # True positive/Prawdziwe pozytywne
  tn = 0.0  # True negative/Prawdziwe negatywne
  fp = 1e-8  # False positive/Fałszywe pozytywne
  fn = 1e-8  # False negative/Fałszywe negatywne
  
  y_pred = []
  y_true = []

  for i, doc in enumerate(textcat.pipe(docs)):
    gold = cats[i]
    for label, score in doc.cats.items():
      if label not in gold:
        continue
      if label == "NOTCYBERBULLY":
        continue
      if score >= 0.5 and gold[label] >= 0.5:
        tp += 1.0
        y_pred.append(True)
        y_true.append(True)
      elif score >= 0.5 and gold[label] < 0.5:
        fp += 1.0
        y_pred.append(True)
        y_true.append(False)
      elif score < 0.5 and gold[label] < 0.5:
        tn += 1
        y_pred.append(False)
        y_true.append(False)
      elif score < 0.5 and gold[label] >= 0.5:
        fn += 1
        y_pred.append(False)
        y_true.append(True)

  counter = Counter(y_pred)
  precision = tp / (tp + fp)
  recall = tp / (tp + fn)
  if (precision + recall) == 0:
      f_score = 0.0
  else:
      f_score = 2 * (precision * recall) / (precision + recall)
  
  return {"precision": precision,
          "recall": recall,
          "f_score": f_score,
          "n_pred_True": counter[True] if True in counter else 0,
          "n_true_True": Counter(y_true)[True]}

from spacy.util import minibatch, compounding
import random
import time

def train(train_data, eval_comments, eval_labels, nlp=None, model=None, epochs=10, dropout=0.2, save_note=''):
  
  if nlp is None:
    if model is not None:
      nlp = spacy.load(model)
      print(f'Wczytano model {model}')
    else:
      nlp = spacy.blank('pl')
      print('Wczytano pusty model "pl".')
  
  if "textcat" not in nlp.pipe_names:
    textcat = nlp.create_pipe("textcat", config={"exclusive_classes": True,
                                                 "architecture": "simple_cnn"})
    nlp.add_pipe(textcat, last=True)
  else:
    textcat = nlp.get_pipe("textcat")

  textcat.add_label("CYBERBULLY")
  textcat.add_label("NOTCYBERBULLY")


  pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
  other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
  with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    
    print("Trenowanie modelu...")


    fmt = '| %5s | %8s | %8s | %8s | %8s | %8s | %10s | %10s |'
    print(fmt % ('Epoch', 'Loss', 'Prec', 'Recall', 'F-score', 'Time (s)', 'pred_bully', 'true_bully'))
    precision = 4
    batch_sizes = compounding(4.0, 32.0, 1.001)
    for epoch in range(epochs):
      start = time.perf_counter()
      losses = {}
      # batch up the examples using spaCy's minibatch
      random.shuffle(train_data)
      batches = minibatch(train_data, size=batch_sizes)
      for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer, drop=dropout, losses=losses)
      with textcat.model.use_params(optimizer.averages):
          # evaluate on the dev data split off in load_data()
          scores = evaluate_texts(nlp.tokenizer, textcat, eval_comments, eval_labels)
      stop = time.perf_counter()
      time_elapsed = stop - start
      
      print(fmt % (epoch,
                   round(losses["textcat"], precision),
                   round(scores["precision"], precision),
                   round(scores["recall"], precision),
                   round(scores["f_score"], precision),
                   round(time_elapsed, 2),

                   scores["n_pred_True"],
                   scores["n_true_True"],
                   ))

  timestamp = round(time.time()*100)
  filename = f'nlp_spacy_model_{timestamp}_{save_note}'
  with nlp.use_params(optimizer.averages):
    nlp.to_disk(filename)
  print(f'> Zapisano model jako {filename}')

  return (nlp, filename)

train_data = train_labels_formatting(training_text_lemmatized, training_labels)

t0 = time.perf_counter()
nlp, filename = train(train_data,
                      test_text,
                      test_labels,
                      nlp=nlp,
                      model=language_model,
                      epochs=5,
                      dropout=0.2,
                      save_note='first')

seconds = round(time.perf_counter() - t0, 4)
minutes = round(seconds/60, 2)

print(f'\n\nCzas trwania {seconds} sekund ~{minutes} minut.')

"""### Ewaluacja

Ewaluacja jest procesem o charakterze praktycznym, którego zadaniem jest ustalenie, czy dany projekt osiągnął zakładane cele. Wyniki zostaną sprawdzone i podjęte zostaną działania, które pozwolą osiągnąć zakładane perspektywy.
"""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from collections import Counter

def predictions_data(nlp, texts, labels):
  y_true = []
  y_pred = []

  for idx, text in enumerate(texts):
    doc = nlp(text)
    is_positive = doc.cats['CYBERBULLY'] >= 0.5
    y_pred.append(int(is_positive))
    y_true.append(int(labels[idx]['CYBERBULLY']))
  print(f'y_true: {Counter(y_true)}')
  print(f'y_pred: {Counter(y_pred)}\n')
  return y_true, y_pred


def accuracy(nlp, texts, labels):
  y_true, y_pred = predictions_data(nlp, texts, labels)
  return accuracy_score(y_true, y_pred)


def print_evaluation_metrics(nlp, texts, labels):
  y_true, y_pred = predictions_data(nlp, texts, labels)
  precision = 2
  acc = round(accuracy_score(y_true, y_pred)*100, precision)
  prec = round(precision_score(y_true, y_pred)*100, precision)
  f1 = round(f1_score(y_true, y_pred)*100, precision)
  rec = round(recall_score(y_true, y_pred)*100, precision)
  
  fmt = '| %10s | %10s | %10s | %10s |'
  print(fmt % ('Accuracy', 'Precision', 'F1-Score', 'Recall'))
  print(fmt % (f'{acc}%', f'{prec}%', f'{f1}%', f'{rec}%'))

print_evaluation_metrics(nlp, test_text, test_labels)

"""## Podejście drugie (klasyfikacja/kategoryzacja): dataset treningowy: 50%, dataset testowy: 50%

### Podział datasetów na sety treningowe oraz tekstowe wraz z wyświetleniem informacji o nich

Wywołanie funkcji importu oraz podział na dataset treningowy oraz testowy ze współczynnikiem testowym 0.5:
"""

(training_text, training_labels), (test_text, test_labels) = load_source_data(0.5)
print((training_text, training_labels), (test_text, test_labels))

"""Pokazanie przykładów datasetu treningowego oraz testowego:"""

limit = 0

print('\nPrzykłady treningowe:')
for (label, text) in zip(training_labels, training_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

limit = 0

print('\nPrzykłady testowe:')
for (label, text) in zip(test_labels, test_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

"""Wyprintowanie liczby zdań treningowych, liczby zdań testowych oraz sumy wszystkich tekstów:"""

sum_number = len(training_labels + test_labels)
print(f'Liczba zdań treningowych: {len(training_text)} ({round(len(training_text)/sum_number *100, 2)}%).')
print(f'Liczba zdań testowych: {len(test_text)} ({round(len(test_text)/sum_number *100, 2)}%).')
print(f'Suma wszystkich zdań: {sum_number}')

"""Sprawdzanie odsetka komentarzy, które są cyberprzemocą oraz które nią nie są dla setu treningowego oraz treningowego i testowego razem:"""

counter = 0
for label in training_labels:
  if label['CYBERBULLY'] == True:
    counter += 1
print(f'Liczba zdań w secie treningowym, które są cyberprzemocą: {counter} ({round(counter/len(training_labels) *100, 2)}%).')

counter_cyberbully = 0
counter_notcyberbully = 0
for label in training_labels + test_labels:
  if label['CYBERBULLY'] == True:
    counter_cyberbully += 1
  else:
    counter_notcyberbully += 1

if counter_cyberbully + counter_notcyberbully == sum_number:
  print(f'Liczba zdań, które nie są cyberprzemocą w obu setach - treningowym i testowym: {counter_notcyberbully} ({round(counter_notcyberbully/sum_number *100, 2)}%).')
  print(f'Liczba zdań, które są cyberprzemocą w obu setach - treningowym i testowym: {counter_cyberbully} ({round(counter_cyberbully/sum_number *100, 2)}%).')

"""### Obróbka datasetów"""

training_text = twitter_clean(training_text)
training_text_lemmatized = lemmatize_train_data(training_text, nlp)
train_data = train_labels_formatting(training_text_lemmatized, training_labels)

"""### Trening"""

t0 = time.perf_counter()
nlp_balanced, filename = train(train_data,
                               test_text,
                               test_labels,
                               nlp=None,
                               model=language_model,
                               epochs=5,
                               dropout=0.2,
                               save_note='second')
seconds = round(time.perf_counter() - t0, 4)
minutes = round(seconds/60, 2)

print(f'\n\nCzas trwania {seconds} sekund ~{minutes} minut.')

"""### Ewaluacja"""

print_evaluation_metrics(nlp_balanced, test_text, test_labels)

"""## Podejście trzecie (klasyfikacja/kategoryzacja): dataset treningowy: 20%, dataset testowy: 80%

### Podział datasetów na sety treningowe oraz tekstowe wraz z wyświetleniem informacji o nich

Wywołanie funkcji importu oraz podział na dataset treningowy oraz testowy ze współczynnikiem testowym 0.8:
"""

(training_text, training_labels), (test_text, test_labels) = load_source_data(0.8)
print((training_text, training_labels), (test_text, test_labels))

"""Pokazanie przykładów datasetu treningowego oraz testowego:"""

limit = 0

print('\nPrzykłady treningowe:')
for (label, text) in zip(training_labels, training_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

limit = 0

print('\nPrzykłady testowe:')
for (label, text) in zip(test_labels, test_text):
  print(f'    Etykieta: {label}')
  print(f'    Tekst: {text}')
  limit += 1
  if limit == 3:
    break

"""Wyprintowanie liczby zdań treningowych, liczby zdań testowych oraz sumy wszystkich tekstów:"""

sum_number = len(training_labels + test_labels)
print(f'Liczba zdań treningowych: {len(training_text)} ({round(len(training_text)/sum_number *100, 2)}%).')
print(f'Liczba zdań testowych: {len(test_text)} ({round(len(test_text)/sum_number *100, 2)}%).')
print(f'Suma wszystkich zdań: {sum_number}')

"""Sprawdzanie odsetka komentarzy, które są cyberprzemocą oraz które nią nie są dla setu treningowego oraz treningowego i testowego razem:"""

counter = 0
for label in training_labels:
  if label['CYBERBULLY'] == True:
    counter += 1
print(f'Liczba zdań w secie treningowym, które są cyberprzemocą: {counter} ({round(counter/len(training_labels) *100, 2)}%).')

counter_cyberbully = 0
counter_notcyberbully = 0
for label in training_labels + test_labels:
  if label['CYBERBULLY'] == True:
    counter_cyberbully += 1
  else:
    counter_notcyberbully += 1

if counter_cyberbully + counter_notcyberbully == sum_number:
  print(f'Liczba zdań, które nie są cyberprzemocą w obu setach - treningowym i testowym: {counter_notcyberbully} ({round(counter_notcyberbully/sum_number *100, 2)}%).')
  print(f'Liczba zdań, które są cyberprzemocą w obu setach - treningowym i testowym: {counter_cyberbully} ({round(counter_cyberbully/sum_number *100, 2)}%).')

"""### Obróbka datasetów"""

training_text = twitter_clean(training_text)
training_text_lemmatized = lemmatize_train_data(training_text, nlp)
train_data = train_labels_formatting(training_text_lemmatized, training_labels)

"""### Trening"""

t0 = time.perf_counter()
nlp_balanced, filename = train(train_data,
                               test_text,
                               test_labels,
                               nlp=None,
                               model=language_model,
                               epochs=5,
                               dropout=0.2,
                               save_note='third')
seconds = round(time.perf_counter() - t0, 4)
minutes = round(seconds/60, 2)

print(f'\n\nCzas trwania {seconds} sekund ~{minutes} minut.')

"""### Ewaluacja"""

print_evaluation_metrics(nlp_balanced, test_text, test_labels)

"""## Regresja (dla podziału 50%/50% danych z klasyfikacji)

Dla podziału równego pomiędzy danymi testowymi, a danymi treningowymi. Zatem regresje wykonamy tylko dla tego przypadku:

### Preprocesing
"""

(training_text, training_labels), (test_text, test_labels) = load_source_data(0.5)
print((training_text, training_labels), (test_text, test_labels))

from sklearn.feature_extraction.text import CountVectorizer

test_text_cleaned = twitter_clean(test_text)
test_text_lemmatized = lemmatize_train_data(test_text_cleaned, nlp)
training_text_cleaned = twitter_clean(training_text)
training_text_lemmatized = lemmatize_train_data(training_text_cleaned, nlp)

cv = CountVectorizer(binary=True)
cv.fit(training_text_lemmatized)
X = cv.transform(training_text_lemmatized)
X_test = cv.transform(test_text_lemmatized)

training_labels_binary = [0 if label['NOTCYBERBULLY'] else 1 for label in training_labels]
test_labels_binary = [0 if label['NOTCYBERBULLY'] else 1 for label in test_labels]

"""### Trening"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import time

parameters = {'solver':('newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'),
              'C':[0.01, 0.1, 1, 2, 4]}

lr = LogisticRegression(n_jobs=-1, max_iter=10000)
clf = GridSearchCV(lr, parameters)

t0 = time.perf_counter()
clf.fit(X, training_labels_binary)
print(f'\n\nTook {round(time.perf_counter() - t0, 2)} second(s).')

print("Best parameter (CV score=%0.3f):" % clf.best_score_)
print(clf.best_params_)

final_model = clf.best_estimator_
final_model.fit(X, training_labels_binary)
print ("Accuracy: %s" % (accuracy_score(test_labels_binary, final_model.predict(X_test))))

"""### Ewaluacja"""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

y_pred = final_model.predict(X_test)

acc = accuracy_score(test_labels_binary, y_pred)
f1 = f1_score(test_labels_binary, y_pred)
prec = precision_score(test_labels_binary, y_pred)
rec = recall_score(test_labels_binary, y_pred)

precision = 2
print (f"Accuracy: {round(acc*100, precision)}%")
print (f"Precision: {round(prec*100, precision)}%")
print (f"f1_score: {round(f1*100, precision)}%")
print (f"Recall: {round(rec*100, precision)}%")

"""### Ewaluacja wskaźników topowych słów"""

feature_to_coef = {
    word: coef for word, coef in zip(cv.get_feature_names(), final_model.coef_[0])}

n = 5
print('Najbardziej obraźliwe:')
for idx, top_cyberbully in enumerate(sorted(feature_to_coef.items(), key=lambda x: x[1], reverse=True)[:n], 1):
   print(f'{idx}) {top_cyberbully}')
    
print('\nNajbardziej neutralne:')
for idx, top_notcyberbully in enumerate(sorted(feature_to_coef.items(), key=lambda x: x[1])[:n], 1):
    print(f'{idx}) {top_notcyberbully}')