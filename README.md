# Kahoot-Replica

𝐈𝐦𝐩𝐨𝐫𝐭𝐚𝐧𝐭 𝐧𝐨𝐭𝐞: This game is BY NO MEANS COMMERCIAL. I am not affiliated with Kahoot at all, I just wanted to make this cool project for whoever would like to run it on their computer for absolutely free. However, I do encourage whoever is running my Kahoot replica to play the real Kahoot and see how similar this is.

𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰:
"Kahoot Replica" is a local multiplayer quiz game to be played on 2 or more separate computers on the same WiFi. This game is inspired by the popular quiz game "Kahoot" because it simulates how Kahoot is played on their website "kahoot.it". Although this project of mine is not a website, it combines Python sockets with Python's library "pygame" to simulate the real version of Kahoot. The goal of the game is to score the most points out of all the players playing by answering each multiple-choice question correctly and quickly.

𝐒𝐤𝐢𝐥𝐥𝐬 𝐮𝐬𝐞𝐝 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐩𝐫𝐨𝐣𝐞𝐜𝐭: 

𝐓𝐨 𝐫𝐮𝐧 𝐭𝐡𝐢𝐬: 
Get 2 or more separate WINDOWS computers on the same WiFi. On both computers: have Python 3 or greater installed, place all of the files in this repository in the same directory by downloading a zip file containing all files in this repository and extracting the zip file to the same directory. On the computer for running the main Kahoot screen, run "server.py" and follow the instructions generated. When the output says "listening for connections," a pygame window should pop up. For anyone who wants to play this as a player, run "client.py" 𝐀𝐅𝐓𝐄𝐑 𝐒𝐄𝐑𝐕𝐄𝐑.𝐏𝐘 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 𝐀𝐍𝐃 𝐓𝐇𝐄 𝐌𝐀𝐈𝐍 𝐁𝐎𝐀𝐑𝐃 𝐏𝐘𝐆𝐀𝐌𝐄 𝐖𝐈𝐍𝐃𝐎𝐖 𝐇𝐀𝐒 𝐏𝐎𝐏𝐏𝐄𝐃 𝐔𝐏 𝐎𝐍 𝐓𝐇𝐄 𝐒𝐄𝐑𝐕𝐄𝐑'𝐒 𝐂𝐎𝐌𝐏𝐔𝐓𝐄𝐑. Then, follow the instructions generated. Also, install the packages "pygame" and "pandas" if these libraries aren't recognized when running either "client.py" or "server.py" or any other packages for libraries that aren't recognized." If you wish to be the kahoot smasher, run "kahoot_smasher.py" and follow the instructions generated. Have fun!

𝐇𝐨𝐰 𝐭𝐨 𝐩𝐥𝐚𝐲 (first view instructions on how to run this above before proceeding):
  𝐀𝐬 𝐭𝐡𝐞 𝐬𝐞𝐫𝐯𝐞𝐫/𝐡𝐨𝐬𝐭: In the pygame window that pops up after entering the Kahoot you wish to play, you can scroll up and down (if players overflow off the screen) using the grey buttons "up" and "down", kick players by clicking their name and hitting the "kick" button, and start the game by pressing "start" at the top right. Ensure that you show all players your screen so they can see each question and the corresponding choices for it. Note: After the game is started, no new players can join it. For each question: you can skip the respective countdown for each question by hitting the "skip" button on the right of the screen. If you do so, whoever has answered correctly will receive points, while those who answered incorrectly or didn't answer before the skip button was pressed will not receive points. After each countdown, hit the "next" button top right to view the leaderboard and "next" again to go to the next question. Repeat for each question and once the top 3 players are shown on the podium, you can stop running "server.py"
  
  𝐀𝐬 𝐚 𝐩𝐥𝐚𝐲𝐞𝐫/𝐜𝐥𝐢𝐞𝐧𝐭: In the pygame window that pops up after entering the IP address of the server, enter a name by spinning the wheel (if random name generator is enabled) or by typing your name (if random name generator isn't enabled). Then, press "Go!" After the host has started the game, look at their screen for each question and answer choices for that question and hit the choice on your computer that you think is right before the countdown hits zero. If you want to leave in the middle of the Kahoot, stop running "client.py" or press x at the top right corner of the pygame window, though know that your name won't be saved and you cannot join back until another game is ready to start.

𝐇𝐨𝐰 𝐭𝐨 𝐦𝐚𝐤𝐞 𝐜𝐮𝐬𝐭𝐨𝐦 𝐤𝐚𝐡𝐨𝐨𝐭 𝐪𝐮𝐢𝐳𝐳𝐞𝐬:
In the "Kahoot Replica folder" which you extracted somewhere on your computer, add your own CSV file to the "quizzes" folder which will represent a new kahoot. The name of the file is the name of that specific kahoot quiz.

𝐇𝐨𝐰 𝐭𝐨 𝐞𝐝𝐢𝐭 𝐚 𝐜𝐮𝐬𝐭𝐨𝐦 𝐤𝐚𝐡𝐨𝐨𝐭 𝐪𝐮𝐢𝐳:
