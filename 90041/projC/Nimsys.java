//package assignment3;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
//import java.io.FileNotFoundException;
import java.io.FileInputStream;
/**
 *  @ STDENT NAME: VINEET SOPPADANDI			STUDENT NUMBER: 888495
 *  
 *  
 */
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.StringTokenizer;

public class Nimsys {

	private static Scanner scannerobject = new Scanner(System.in);

	private NimPlayer[] player;												// Max 100 player provided by the assignment sheet therefore creating array object with 100 elements


	public static void main(String[] arg){

		System.out.println("Welcome to Nim");								//welcome message
		System.out.println();

		int counter = 0;
		Nimsys terminal = new Nimsys();
		terminal.player = new NimPlayer[101];								//allocating 101 elements - reason 101 is because it makes it easier to perform operations on array

			
		
		while(true){
			
			FileInputStream fis = null;
			try {
				fis = new FileInputStream("players.ser");
				ObjectInputStream ois = null;
				try {
					ois = new ObjectInputStream(fis);
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				
				try {
					terminal.player = (NimPlayer[]) ois.readObject();
					//System.out.print(player[1].getFamily_name());
				} catch (ClassNotFoundException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				try {
					ois.close();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			
			} catch (FileNotFoundException e2) {

			}
			
			
			
			String buffer = null;
			String userInput = null;
			System.out.print("$");

			userInput = scannerobject.nextLine();									// Txt interference scanning for user input 

			StringTokenizer token = new StringTokenizer(userInput, " ,");

			String userTxt= token.nextToken(); 										// get the command from the user e.g. addplayer, removeplayer etc..

			try {
			
				
				if(userTxt.equals("exit")){										// exit command called by user

				
				FileOutputStream file = new FileOutputStream("players.ser");
				ObjectOutputStream obFile = new ObjectOutputStream(file);
				
				obFile.writeObject(terminal.player);
				obFile.close();
				
				System.out.println();			
				terminal.exit();
			}

			else if(userTxt.equals("addplayer")){							// addplayer call by user

				int c	= token.countTokens();								// counting the number of inputs

				if(c<3){

					throw new Exception("Incorrect number of arguments supplied to command.");

				}

				String uN = token.nextToken();								// scaning username
				String fN = token.nextToken();								// scaning username
				String gN = token.nextToken();								// scaning username

				terminal.addplayer(uN,gN,fN, true);
				System.out.println();
			}

			
			else if(userTxt.equals("addaiplayer")){							// addplayer call by user

				int c	= token.countTokens();								// counting the number of inputs

				if(c<3){

					throw new Exception("Incorrect number of arguments supplied to command.");

				}

				String uN = token.nextToken();								// scaning username
				String fN = token.nextToken();								// scaning username
				String gN = token.nextToken();								// scaning username

				terminal.addplayer(uN,gN,fN, false);
				System.out.println();
			}

			
			
			else if(userTxt.equals("removeplayer")){						//removeplayer called by user

				int c	= token.countTokens();								// counting the number of inputs
				String uN = null;								

				if(c==1){													
					uN = token.nextToken();								// scanning username input
				}

				terminal.removeplayer(uN,c, scannerobject);
				System.out.println();
				//buffer = scannerobject.nextLine();
			}


			else if(userTxt.equals("editplayer")){							//edit player called

				int c	= token.countTokens();
				
				if(c<3){

					throw new Exception("Incorrect number of arguments supplied to command.");

				}

				String uN = token.nextToken();								// scaning username
				String new_fN = token.nextToken();							// scaning new given name
				String new_gN = token.nextToken();							// scaning new family name

				terminal.editplayer(uN,new_gN,new_fN);
				System.out.println();

			}

			else if(userTxt.equals("resetstats")){							//calling resetstats

				int c = token.countTokens();								// counting tokens
				String uN = null;
				if(c==1){								
					uN = token.nextToken();									
				}

				terminal.resetstats(uN, c, scannerobject);
				System.out.println();

			}

			else if(userTxt.equals("displayplayer")){						//displayer called by user

				int c = token.countTokens();								//counting tokens
				String uN = null;	
				if(c==1){

					uN = token.nextToken();
				}

				terminal.displayer(uN, c);
				System.out.println();

			}

			else if(userTxt.equals("rankings")){							//rankings called by user

				NimPlayer[] sort = terminal.player;							//created an array of objects "sort"
				String order=null;

				int c = token.countTokens();								//counting tokens

				if(c==1){
					order = token.nextToken();								//scanning the order
				}

				terminal.ranking(order, c, sort);
				System.out.println();
			}

			else if(userTxt.equals("startgame")){									//calling start game

				int currentStone=Integer.parseInt(token.nextToken());				// storing the values of the user input for starting game
				int upperBound=Integer.parseInt(token.nextToken());					
				String player1=(token.nextToken());
				String player2=token.nextToken();

				terminal.startgame(currentStone, upperBound, player1, player2);
				System.out.println();

			}

			else{

				throw new Exception("'"+userTxt+"'"+" is not a valid command.");
				

			}
			counter++;
			if(counter == 1000){
				break;
			}
			}catch(Exception e){
				System.out.println(e.getMessage());
				System.out.println();
				
			}
		}
	}

	////////////////////////-------------------ADD PLAYER---------------------------------------///////////////

	private void addplayer(String uN,String gN,String fN, boolean isHumanPlayer){
		int j = 0;
		int i =0;

		for(i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]==null){
				j=i;
				break;
			}
		}

		if(j==0){
			if(isHumanPlayer)
				player[j] = new NimHumanPlayer(uN, gN, fN);						// for initial player
			else
				player[j] = new NimAIPlayer(uN, gN, fN);
		}


		else{ 

			for(i = 0;i<j;i++){														// Forloop made to check the usernames existence
				if((player[i].getUser_name()).equals(uN)){
					System.out.println("The player already exists.");

					player[j]=null;
					break;
				}

				else{
					if(isHumanPlayer)
						player[j] = new NimHumanPlayer(uN, gN, fN);
					else
						player[j] = new NimAIPlayer(uN, gN, fN);
				}

			}
		}
	}

	////////////////////////-------------------REMOVE PLAYER---------------------------------------///////////////

	private void removeplayer(String uN, int tokens, Scanner scan){

		int eleNull =0;
		int plyPresent =0;
		//--------------------------------------------------------------------------------------------------------------------------------//
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]!=null){
				plyPresent=i;
			}

			else if(player[i]==null){

				eleNull=i;
				break;	
			}
		}
		//--------------------------------------------------------------------------------------------------------------------------------//

		if(tokens==1 && uN!=null)	{														

			if(plyPresent==0 && tokens ==0){									//case of only one player
				player[plyPresent] = null;
			}

			else {

				for(int i = 0;i<eleNull;i++){										// Forloop made to check the usernames existence

					if(player[i].getUser_name().equals(uN)){

						if(i==plyPresent){
							player[i] = null;
						}

						else{
							player[i] = null;										//removing and replacing the player with the last player
							player[i] = player[plyPresent];
							player[plyPresent] = null;
							plyPresent--;

						}
						break;
					}

					else if(i==plyPresent){										// player not exisiting
						System.out.println("The player does not exists.");
					}
				}
			}
		}

		else if(tokens==0){																	// case of removing all players

			System.out.println("Are you sure you want to remove all players? (y/n)");

			String answer = scan.nextLine();

			if(answer.equals("y")){

				for(int i=0; i<eleNull;i++){
					player[i] = null;
				}
			}
		}
	}

	////////////////////////-------------------EDIT PLAYER---------------------------------------///////////////

	private void editplayer(String uN, String new_gN, String new_fN){

		//--------------------------------------------------------------------------------------------------------------------------------//
		int eleNull =0;
		int plyPresent =0;
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]!=null){
				plyPresent=i;
			}

			else if(player[i]==null){

				eleNull=i;
				break;	
			}
		}

		//--------------------------------------------------------------------------------------------------------------------------------//

		for(int i = 0;i<eleNull;i++){														// Forloop made to check the usernames existence

			if((player[i].getUser_name()).equals(uN)){

				player[i].setGiven_name(new_gN);
				player[i].setFamily_name(new_fN);

				break;
			}

			else if(i==plyPresent){
				System.out.println("The player does not exists.");
			}
		}
	}

	////////////////---------------------------RESETSTATS--------------------------------------///////////////

	private void resetstats(String uN, int t, Scanner scan){

		//----------------------------------------------------------------------------------------------------//
		int eleNull =0;
		int plyPresent =0;
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]!=null){
				plyPresent=i;
			}

			else if(player[i]==null){

				eleNull=i;
				break;	
			}
		}

		//----------------------------------------------------------------------------------------------------//

		if(t==1 && uN!=null){

			for(int i = 0;i<eleNull;i++){														// Forloop made to check the usernames existence

				if(player[i].getUser_name().equals(uN)){

					player[i].setGames_played(0);
					player[i].setGames_won(0);

					break;
				}

				else if(i==plyPresent){															//case username does not exist
					System.out.println("The player does not exists.");
				}
			}
		}

		else if(t==0){																	// case to reset all stats for all players

			System.out.println("Are you sure you want to reset all player statistics? (y/n)");

			String answer = scan.nextLine();

			if(answer.equals("y")){

				for(int i=0; i<eleNull;i++){

					player[i].setGames_played(0);
					player[i].setGames_won(0);
				}
			}
		}
	}

	///////////////----------------------------DISPLAYER---------------------------------------///////////////	

	private void displayer(String uN, int t){

		int j =0;
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]==null){

				j=i;
				break;
			}
		}

		if(t==1 && uN!=null) {

			for(int i = 0;i<j;i++){														// Forloop made to check the usernames existence

				if(player[i].getUser_name().equals(uN)){

					System.out.println(player[i].getUser_name()+","+player[i].getGiven_name()+","+player[i].getFamily_name()+","+player[i].getGames_played()+" games,"+player[i].getGames_won()+" wins");

					break;
				}

				else if(i==j-1){
					System.out.println("The player does not exists.");			// printing when user name is not present
				}
			}
		}
		else if(t==0){															// condition for displaying all user names

			for(int k=0; k<j;k++){
				System.out.println(player[k].getUser_name()+","+player[k].getGiven_name()+","+player[k].getFamily_name()+","+player[k].getGames_played()+" games,"+player[k].getGames_won()+" wins");
			}
		}
	}

	////////////////////////-------------------RANKING-----------------------------------------///////////////

	private void ranking(String order,int t, NimPlayer[] sort){


		//----------------------------------------------------------------------------------------------------//
		int eleNull =0;
		int plyPresent =0;
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]!=null){
				plyPresent=i;
			}

			else if(player[i]==null){

				eleNull=i;
				break;	
			}
		}

		//----------------------------------------------------------------------------------------------------//
		sort(sort,plyPresent);								//calling sort method

		if(t==1 && order.equals("asc")){					// asc order selected to display rankings

			for(int i = plyPresent; i>=0;i--){					// forloop designed to print the elements backwards as the sort method sorts players score in decensing order
				double percent=0;

				if(sort[i].getGames_played() ==0){ 				// condition made to avoid dividing by 0
					percent = 0;
				}
				else{ 
					percent = ((double)sort[i].getGames_won()/(double)sort[i].getGames_played())*100;
				}
				String give_name = sort[i].getGiven_name();
				String fam_name = sort[i].getFamily_name();

				String game_played=String.format("%02d",sort[i].getGames_played());				
				String percentage=String.format("%d",(int)percent);
				System.out.println(percentage+"%"+" | "+game_played+" | "+give_name+" "+fam_name);

			}
		}

		else if(t==0){											// case of desending order is required and by default desending order

			if(order ==null ||order.equals("desc") ){

				for(int i = 0; i<eleNull;i++){
					double percent=0;

					if(sort[i].getGames_played() ==0){					//case of games played is 0 to avoid division by zero error
						percent = 0;
					}
					else{ 
						percent = ((double)sort[i].getGames_won()/(double)sort[i].getGames_played())*100;
					}
					String give_name = sort[i].getGiven_name();
					String fam_name = sort[i].getFamily_name();

					String game_played=String.format("%02d",sort[i].getGames_played());				
					String percentage=String.format("%d",(int)percent);
					System.out.println(percentage+"%"+" | "+game_played+" | "+give_name+" "+fam_name);

				}
			}
		}
	}

	////////////////////////-------------------EXIT--------------------------------------------///////////////

	private void exit(){
		// This exits the program while in idle state
		System.exit(0);
	}

	////////////////////////-------------------STARTGAME---------------------------------------///////////////

	private void startgame(int initialStones, int upperBound, String uN1, String uN2){



		//----------------------------------------------------------------------------------------------------//
		int eleNull =0;
		int plyPresent =0;
		for(int i =0;i<player.length;i++){ 									// checking how many elements (players) are present

			if(player[i]!=null){
				plyPresent=i;
			}

			else if(player[i]==null){

				eleNull=i;
				break;	
			}
		}

		//----------------------------------------------------------------------------------------------------//

		int p1_index = 0;
		int p2_index = 0;
		int counter = 0;
		for(int i =0; i<eleNull;i++){

			if(player[i].getUser_name().equals(uN1)){									//checking the username 1 index

				p1_index = i;
				counter++;

			}

			if(player[i].getUser_name().equals(uN2)){									//checking the username 2 index

				p2_index = i;
				counter++;
			}

			NimGame game = new NimGame(initialStones, upperBound, player[p1_index], player[p2_index]);	// creating NimGame instance

			if(counter==2){

				game.startgame(scannerobject);
				break;
			}

			else if(i==plyPresent){										// case of payer does not exist
				System.out.println("One of the players does not exist.");
			}
		}
	}

	/////////////////-------------------------------------------------------------------------///////////////
	/**
	 * kindly note the sorting code below is adapted from the lecture notes 
	 * */
	private void sort(NimPlayer[] a, int numberUsed){

		int index, indexOfNextSmallest;

		if(numberUsed >10){
			numberUsed =10;
		}

		for(index = 0; index < numberUsed; index++){

			indexOfNextSmallest = indexOfSmallest(index,a,numberUsed);

			interchange(index,indexOfNextSmallest,a);
		}
	}

	private static int indexOfSmallest(int startIndex, NimPlayer[] a, int numberUsed){

		int min=0;  

		if(a[startIndex].getGames_played()==0){
			min =0;
		}
		else{
			min=(int) (((double)a[startIndex].getGames_won())/(double)(a[startIndex].getGames_played()))*100;
		}

		int indexOfMin = startIndex;
		int index;
		int min_2=0;
		for(index = startIndex+1;index< numberUsed+1;index++){

			if((a[index].getGames_played())==0){
				min_2=0;
				indexOfMin = index;
			}

			else{ 
				min_2 =((a[index].getGames_won())/(a[index].getGames_played()));
			}

			if(min_2 >0 && min_2<min){

				min = ((a[index].getGames_won())/(a[index].getGames_played()));
				indexOfMin = index;
			}

			else{
				indexOfMin = startIndex;
			}
		}

		return indexOfMin;
	}

	private static void interchange(int i, int j, NimPlayer[] a){

		NimPlayer temp;
		temp = a[i];
		a[i] = a[j];
		a[j] = temp;
	}
}
