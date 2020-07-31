//package Assignment_1;

/**
 * 
 * @ STDENT NAME: VINEET SOPPADANDI			STUDENT NUMBER: 888495
 * NimPlayer used to return the value of stones to be removed by the respective player
 */

import java.util.Scanner;

public class NimPlayer {																			  // Player class called NimPlayer

	public String name;																				    // instance "name" to obtain the name of the players 
	int removeStones; 
		public int removestones(Scanner n){													// method created to get the number of stones that need to be removed
		System.out.println(name +"'s turn - remove how many?");
 
		removeStones = n.nextInt();															  // remove_stones variable used to store use input of stones to remove
		return removeStones;																		    // method returns the numbers of stones the player wants to remove
	}
}

