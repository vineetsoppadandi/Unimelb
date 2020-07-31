//package Assignment_1;

/**
 * Nimsys file, a Nim game where each player takes the number to stones with out exceeding the upper bound. 
 * The player removing the last stone is the looser and the other is the winner. 
 * This games logic in written in code to be played on computer using JAVA
 * Takes the details of 2 players
 * sets the upper bound and the initial number of stones at the start
 * Each players get a turn to remove the stones unitll none are left
 * @ STDENT NAME: VINEET SOPPADANDI			STUDENT NUMBER: 888495
 *
 */

import java.util.Scanner;
public class Nimsys {

	public static void main(String[] arg){

		Scanner scannerobject = new Scanner(System.in); 		                              // creating object scannerobject

		System.out.println("Welcome to Nim");   		                                      // Introduction to Nim game
		System.out.println();
		System.out.println("Please enter Player 1's name:");
		String player1 = scannerobject.next();					                                  // Input for Player 1 name 

		NimPlayer p1 = new NimPlayer();							                                      // Creating p1 object
		p1.name = player1;										                                            // storing player 1 name in p1 object
		System.out.println();

		System.out.println("Please enter Player 2's name:");
		String player2 = scannerobject.next();					                                  // Input for player 2 name 

		NimPlayer p2 = new NimPlayer();							                                      // creating p2 object
		p2.name = player2;										                                            // Storing p2 name 
		System.out.println();

		for(int i = 0;i<1000;i++){												                                // Forloop used to make the game continue when player wants to play again.
			System.out.println("Please enter upper bound of stone removal:");
			int b = scannerobject.nextInt();							                                  // User input the upper bound, variable denoted as Upper_Bound

			System.out.println();
			System.out.println("Please enter initial number of stones:");		
			int iniStones = scannerobject.nextInt();							                          // User input for initial stones, variable denoted as ini_stones

			System.out.println();
			System.out.print(iniStones + " stones left:");						                      // print number of stones " *"
			for(int star=1; star<=iniStones;star++){
				System.out.print(" *");
			}

			int rStones = iniStones;											                                  // R_stones = total remaining stones
			for(int j = 0;j<1000;j++){											                                // Forloop used to make the players have multiple turns un till the game is over.

				System.out.println();
				int rmovestones= p1.removestones(scannerobject);						                  // The game starts with player1, requires input from player to remove stones
				rStones = rStones - rmovestones;									                            // r_stones variable denotes the number stones player wants to remove 
				System.out.println();
				if(rStones!=0){												                                        // Conditiion such that it will not print "0 stones left"
					System.out.print(rStones + " stones left:");
				}
				for(int star=1; star<=rStones;star++){							                          // print number of stones " *"
					System.out.print(" *");
				}

				if(rStones==0){												                                        // when no stones are left
					System.out.println("Game Over");
					System.out.println(p2.name+" wins!");
					break;
				}

				System.out.println();
				rmovestones = p2.removestones(scannerobject);						                      // r_stones variable denotes the number stones player wants to remove
				rStones = rStones - rmovestones;
				System.out.println();

				if(rStones!=0){                                                               // Conditiion such that it will not print "0 stones left"
					System.out.print(rStones + " stones left:");				
				}
				for(int star=1; star<=rStones;star++){							                          // print the number of stones left by this symbol " *"
					System.out.print(" *");
				}

				if(rStones==0){												                                        // When there are no stones left
					System.out.println("Game Over");
					System.out.println(p1.name+" wins!");
					break;
				}
			j++;																                                            // safety net variable
			}

			System.out.println();
			System.out.print("Do you want to play again (Y/N):"); 	                        // requires user input to restart/exit the game

			String response = scannerobject.next();

			if(!(response.equals("Y"))){										                                // The response given by the user is not "Y" the program will exit
				System.exit(0);
			}
      System.out.println();
		i++;																	                                            // safety net variable
		}
	}
}

