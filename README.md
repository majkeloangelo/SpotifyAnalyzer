Setup
1.	Make sure you’ve installed Python, Docker and IDE like PyCharm or Visual Studio Code
2.	Clone this repository in the folder of your preference, and then enter that folder:

        git clone https://github.com/majkeloangelo/SpotifyAnalyzer

        cd SpotifyAnalyzer
  	
5.	Open IDE and load project
6.	Install all required dependencies like Pandas, PyQt5 and Psycopg2
7.	Run CMD and enter directory from point 2 and build container with database:

  	    docker build -t postgres -f dockerfile.dockerfile .

  	    docker run --name spotifyanalyzer -p 5432:5432 -d postgres

Run and test 
1.	Run python script in IDE
2.	In desktop application load data with “load data…" button 
3.	You can load your own streaming history witch u can get from Spotify (download your extended streaming history from the Privacy Settings in your Spotify account) or you can also load sample.json from downloaded directory with code



