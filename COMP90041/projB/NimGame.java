//package Assignment_2;

/**
 *  @ STDENT NAME: VINEET SOPPADANDI			STUDENT NUMBER: 888495
 */

import java.util.Scanner;

public class NimGame {																				// Player class called NimGame

	private int currentStone;																		//instances of the class NimGame
	private int upperBound;
	private NimPlayer player1;
	private NimPlayer player2;
	private int removeStones;

	public NimGame(int startStone, int startBound, NimPlayer playerOne, NimPlayer playerTwo) {
		currentStone = startStone;
		upperBound = startBound;
		player1 = playerOne;
		player2 = playerTwo;
	}

	void startgame(Scanner input){
		String buffer = null;
		player2.setGames_played(player2.getGames_played() +1);									// increasing the games played the respective players
		player1.setGames_played(player1.getGames_played() +1);
		System.out.println();
		
		System.out.println("Initial stone count: "+currentStone);										// Printing out the rules and player information 
		System.out.println("Maximum stone removal: "+upperBound);
		System.out.println("Player 1: "+player1.getGiven_name() + " "+player1.getFamily_name());
		System.out.println("Player 2: "+player2.getGiven_name() + " "+player2.getFamily_name());

		System.out.println();
			
		int iniStones = currentStone;							                          // User input for initial stones, variable denoted as ini_stones
		int rmovestones=0;
		int rStones = iniStones;
		int upBound = upperBound;

		for(int j = 0;j<1000;j++){											                                // Forloop used to make the players have multiple turns un till the game is over.
			buffer = null;
			
			upBound = upperBound;

			while(true){
				if(rStones!=0){                                                              // Conditiion such that it will not print "0 stones left"
					System.out.print(rStones + " stones left:");				
				}
				for(int star=1; star<=rStones;star++){							                          // print the number of stones left by this symbol " *"
					System.out.print(" *");
				}

				System.out.println();					

				rmovestones= removestones(input, player1);						                      // The game starts with player1, requires input from player to remove stones

				if(rStones<upBound ){
					upBound=rStones;
				}
				if(rmovestones>upBound || rmovestones==0){											// checking for invalid input of removing stones
					System.out.println();
					System.out.println("Invalid move. You must remove between 1 and " +upBound +" stones");
					System.out.println();
				}

				else{
					break;
				}
			}
			rStones = rStones - rmovestones;									                              // r_stones variable denotes the number stones player wants to remove 

			if(rStones==0){												                                      // when no stones are left
				System.out.println();
        System.out.println("Game Over");
				System.out.println(player2.getGiven_name()+" "+player2.getFamily_name()+" wins!");
        
				player2.setGames_won(player2.getGames_won() +1) ; 
				buffer = input.nextLine();
				break;
			}

			System.out.println();
			while(true){
				if(rStones!=0){                                                              // Conditiion such that it will not print "0 stones left"
					System.out.print(rStones + " stones left:");				
				}
				for(int star=1; star<=rStones;star++){							                          // print the number of stones left by this symbol " *"
					System.out.print(" *");
				}

				System.out.println();
				rmovestones = removestones(input, player2);						                        // r_stones variable denotes the number stones player wants to remove

				if(rStones<upBound ){
					upBound=rStones;
				}

				if(rmovestones>upBound || rmovestones==0){
					System.out.println();
					System.out.println("Invalid move. You must remove between 1 and " +upBound +" stones");	// checking for invalid input of removing stones
					System.out.println();
				}

				else{
					break;
				}
			}
			rStones = rStones - rmovestones;
			System.out.println();

			if(rStones==0){												                                      // When there are no stones left
				System.out.println();
        System.out.println("Game Over");
				System.out.println(player1.getGiven_name()+" "+player1.getFamily_name()+" wins!");
        
				player1.setGames_won(player1.getGames_won() +1) ;
				buffer = input.nextLine();
				
				break;
			}
		}
	}

	private int removestones(Scanner n, NimPlayer player){													// method created to get the number of stones that need to be removed
		System.out.println(player.getGiven_name() +"'s turn - remove how many?");

		removeStones = n.nextInt();															  // remove_stones variable used to store use input of stones to remove
		return removeStones;																		    // method returns the numbers of stones the player wants to remove

	}

}

