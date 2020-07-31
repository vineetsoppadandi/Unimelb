//package assignment3;

import java.util.Scanner;

public class NimHumanPlayer extends NimPlayer{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public NimHumanPlayer(String userName, String givenName, String familyName) {
		
		super(userName, givenName, familyName);
		// TODO Auto-generated constructor stub
	}

	public int removestones(Scanner n,int max, int remainng){													// method created to get the number of stones that need to be removed
		int removeStones;
		
		System.out.println(getGiven_name() +"'s turn - remove how many?");
		removeStones = n.nextInt();															  // remove_stones variable used to store use input of stones to remove
		return removeStones;																		    // method returns the numbers of stones the player wants to remove
	}
	
}
