//package assignment3;

import java.util.Scanner;

public class NimAIPlayer extends NimPlayer{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public NimAIPlayer(String userName, String givenName, String familyName) {
		super(userName, givenName, familyName);
		// TODO Auto-generated constructor stub
	}
	
	public int removestones(Scanner n, int max, int remainng){													// method created to get the number of stones that need to be removed
	
		int k;
		int removeStones = 0;
		
		k = ((remainng)-1) % (max+1);
		
		if(k!=0 || remainng < max){
			removeStones = 1;
		}
		
		else if( k ==0 ){
			
			while(true){
				
				removeStones = remainng - k*(max+1)+1;
				
				if(removeStones <max && removeStones >0){
					
					break;
				}
				k++;
				}
			
		}
		
		
		//removeStones=1;	
		System.out.println(getGiven_name() +"'s turn - remove how many?");
																	  // remove_stones variable used to store use input of stones to remove
		return removeStones;																		    // method returns the numbers of stones the player wants to remove
	}
}
