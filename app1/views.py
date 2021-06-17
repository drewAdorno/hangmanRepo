from django.shortcuts import render, redirect
import random
from . import words
from .models import *

def index(request):
    if 'score' not in request.session:
        request.session['score']=0
    if 'word' not in request.session:
        if 'difficulty' not in request.session or request.session['difficulty'] == 'easy':
            request.session['word']=words.easy[random.randint(0, len(words.easy)-1)]
            print(request.session['word'])
        elif request.session['difficulty'] == 'med':
            request.session['word']=words.med[random.randint(0, len(words.med)-1)]
            print(request.session['word'])
        else:
            request.session['word']=words.hard[random.randint(0, len(words.hard)-1)]
            print(request.session['word'])
        request.session['word2']=request.session['word']
        request.session['masked_word']= "_" * len(request.session['word'])
        request.session['remainingGuesses']=10
        request.session['status']='ongoing'
        request.session['picture']=f'images/{request.session["remainingGuesses"]}.jpg'
        request.session['placeholder']=[]
        request.session['lettersGuessed']=[]
        
    context={
        'numGuesses':request.session["remainingGuesses"]
    }

    return render(request, 'index.html', context)

def letter(request):     
        letter=request.POST['letter'].lower()  #make letter lowercase
        result = request.session['word2'].find(letter)   #see if letter is in the word
        if result == -1:    #if its not in the word
            letter=letter.upper()   #make a n
            request.session['lettersGuessed'].append(letter)
            request.session['remainingGuesses'] -= 1
            request.session['picture']=f'images/{request.session["remainingGuesses"]}.jpg'
            result_check(request)
            return redirect('/')
        while(request.session['word2'].find(letter) != -1):
            result = request.session['word2'].find(letter)
            request.session['word2'] =request.session['word2'][0:result] + " " + request.session['word2'][result + 1:]
            temp = request.session['masked_word'][0:result] + letter + request.session['masked_word'][result + 1:]
            request.session['masked_word'] = temp
            print(request.session['word2'])
        result_check(request)
        return redirect('/')

def result_check(request):
    if request.session['word'] == request.session['masked_word']:
        request.session['status'] = 'win'
        if request.session['difficulty'] == 'easy':
            request.session['score']=100
        elif request.session['difficulty'] == 'med':
            request.session['score']=500
        else:
            request.session['score']=1000
    if request.session['remainingGuesses'] == 1:
        request.session['status']='lose'
        print(request.session['masked_word'])
        for i in range(len(request.session['masked_word'])):
            if(request.session['masked_word'][i]=='_'):
                request.session['placeholder'].append([request.session['word'][i],'text-danger'])
            else:
                request.session['placeholder'].append([request.session['word'][i],''])
        print(request.session['placeholder'])

def newGame(request, difficulty):
    request.session.clear()
    request.session['difficulty']=difficulty
    return redirect('/')

def leaderboard(request):
    context={
        'scores':Score.objects.all().order_by('-score')
    }
    return render(request, 'leaderboard.html', context)

def addScore(request):
    Score.objects.create(name=request.POST['name'], score=request.POST['score'])
    dif=request.session['difficulty']
    return redirect(f'/leaderboard')