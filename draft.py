import os
import random
os.environ['TERM'] = 'xterm'

strings =  {
    'input_decks_length': 'Введите количество колод: ',
    'play_again': 'Хотите сыграть снова? (да/нет):',
    'casino_always_wins': 'Казино всегда выигрывает!',
    'result_title': '\n*** РЕЗУЛЬТАТЫ РАУНДА ***\n',
    'dealer_hand': 'У раздающего на руке: ',
    'player_hand': 'У вас на руке: ',
    'in_sum': 'в сумме: ',
    'win': 'Поздравляю, у вас больше очков, чем у раздающего. Вы выиграли!\n',
    'win_21': 'Поздравляю! У вас 21, вы выиграли!\n',
    'blackjack_win': 'Поздравляю! У вас блек-джек, вы выиграли!\n',
    'lose': 'У раздающего больше очков, чем у вас. Вы проиграли.\n',
    'lose_21': 'Простите, вы проиграли. У раздающего 21.\n',
    'blackjack_lose': 'Простите, вы проиграли. У раздающего блек-джек.\n',
    'tie': 'Раздающий набрал столько же, сколько и вы. В этом раунде победителя нет.\n',
    'blackjack_tie': 'У вас и у раздающего блек-джек. В этом раунде победителя нет.\n',
    'new_game': "\n    Новая игра!\n",
    'lose_title': 'ПОРАЖЕНИЯ',
    'win_title': 'ПОБЕДЫ',
    'dealer_card_show': 'Раздающий показывает ',
    'player_hand_show_1': 'У вас на руке: ',
    'player_hand_show_2': ', в сумме количество очков равно ',
    'player_score': 'Сумма ваших очков: ',
    'dealer_hit_card': 'Раздающий взял новую карту. У него на руках: ', 
    'invalid_command': "Неверный ввод. Пожалуйста, введите 'д', 'о' или 'в'.",
    'select_command': 'Вы хотите [д]обрать карту, [о]становиться или [в]ыйти из игры?',
}

decks = input(strings['input_decks_length'])
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * (int(decks) * 4)
titles = {11: 'J', 12: 'Q', 13: 'K', 14: 'A',}
command = {'д': 'add', 'о': 'stop', 'в': 'exit', 'да': 'yes' }

wins = 0
losses = 0

def formatText(text, bold = 0, color = 37, background = 40):
    return f"\033[{bold};{color};{background}m{text}"

def clearText():
    return "\033[0m"

def separator():
    return "-" * 30 + "\n"

def tab():
    return '   '

def deal(deck):
   hand = []
   random.shuffle(deck)
   
   for i in range(2):
       card = deck.pop()
       hand.append(card)
   return hand

# функция запуска нового раунда игры после окончания предыдущего
def checkPlayAgain():
   again = input(strings['play_again']).lower()
   
   if command.get(again) == 'yes':
       game()
   else:
       print(formatText(strings["casino_always_wins"], 0, 35, 40) + clearText())
       exit()

# функция подсчёта очков по картам на руке
def total(hand):
   points = 0
   
   for card in hand:
        points += card
   
   return points

# функция добавления новой карты
def hit(hand):
   card = deck.pop()
   hand.append(card)
   return hand

def decorateHand(hand):
    global titles
    decoratedHand = []

    for card in hand:
        decoratedHand.append(titles.get(card) if titles.get(card) else str(card))

    return decoratedHand

# функция вывода результатов
def printResults(dealer_hand, player_hand):
   print(strings['result_title'] + "\n")
   print(strings['dealer_hand'] + str(decorateHand(dealer_hand)) + "," + strings['in_sum'] + str(total(dealer_hand)) + "\n")
   print(strings['player_hand'] + str(decorateHand(player_hand)) + "," + strings['in_sum'] + str(total(player_hand)) + "\n")

# функция подсчёта очков
def checkGameOver(dealer_hand, player_hand, first_step = False):
   global wins
   global losses

   printResults(dealer_hand, player_hand)
   
   if total(player_hand) > 21:
       print('У вас перебор')
       losses += 1
       checkPlayAgain()
       return    
   
   if total(dealer_hand) > 21:
       print('У раздающего перебор, вы выиграли!')
       wins += 1
       checkPlayAgain()
       return

   if total(player_hand) < total(dealer_hand):
       print(strings['lose'])
       losses += 1
       return
   
   if total(player_hand) > total(dealer_hand):
       print(strings['win'])
       wins += 1
       return

   if total(player_hand) == 21:
       print(first_step if strings['blackjack_win'] else strings['win_21'])
       wins += 1
   
   if total(dealer_hand) == 21:
       print(first_step if strings['blackjack_lose'] else strings['lose_21'])
       losses += 1
   
   if total(dealer_hand) == total(player_hand):
       print(first_step if strings['blackjack_tie'] else strings['tie'])
   
   if(first_step):
       checkPlayAgain()

# основная функция игры
def game():
   global wins
   global losses
   
   #выводим информацию о начале игры
   print(strings['new_game'])
   print(separator())
   print(tab() + formatText(strings["win_title"], 1, 32, 40))
   print(tab() + formatText(str(wins), 1, 37, 40))
   print(tab() + formatText(strings["lose_title"], 1, 31, 40))
   print(tab() + formatText(str(losses), 1, 37, 40))
   print(clearText() + "\n")
   print(separator())

   #раздаём карты и выводим в консоль
   dealerHand = deal(deck)
   playerHand = deal(deck)
   print(strings['dealer_card_show'] + str(decorateHand(dealerHand)[0]))
   print(strings['player_hand_show_1'] + str(playerHand) + strings['player_hand_show_2'] + str(total(playerHand)))
   
   # проверяем, есть ли у кого-то 21
   checkGameOver(dealerHand, playerHand, True)

   while True:
       # спрашиваем у игрока, что он хочет сделать
       choice = input(formatText(strings['select_command'], 1, 33, 40) + clearText()).lower() 

       if(command.get(choice) == None):
           print(strings['invalid_command'])

        # если игрок решил завершить игру, выводим сообщение и завершаем программу
       if command.get(choice) == 'exit':
           print(formatText(strings["casino_always_wins"], 0, 35, 40) + clearText())
           exit()

       # при выборе добрать карту
       if command.get(choice) == 'add':
           # запускаем функцию добавления карты выводим новый список карт и сумму очков
           hit(playerHand)
           print(decorateHand(playerHand))
           print(strings['player_score'] + str(total(playerHand)))            

       # при выборе остановиться ход переходит раздающему пока у дилера меньше 17 очков, он должен добирать карты
       if command.get(choice) == 'stop':
           while total(dealerHand) < 17:
               hit(dealerHand)
               print(strings['dealer_hit_card'], dealerHand)
           
       checkGameOver(dealerHand, playerHand)       

# запускаем основную функцию игры
game()