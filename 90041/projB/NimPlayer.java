//package Assignment_2;

/**
 *  @ STDENT NAME: VINEET SOPPADANDI			STUDENT NUMBER: 888495
 */

public class NimPlayer {																			  // Player class called NimPlayer

		private String user_name;																	//instances of the class NimGame 
		private String given_name;
		private String family_name;		
		private int games_played;
		private int games_won;
		
		
		
		public NimPlayer(String userName, String givenName, String familyName){

			user_name =userName;																				     
			given_name = givenName;
			family_name = familyName;		
			games_played = 0;
			games_won = 0;

		}
		
		
	
//Geters and seters are made for a class to be able to acess the variables from NimGame

		public int getGames_played() {
			return games_played;
		}


		public void setGames_played(int games_played) {
			this.games_played = games_played;
		}


		public int getGames_won() {
			return games_won;
		}


		public void setGames_won(int games_won) {
			this.games_won = games_won;
		}


		public String getUser_name() {
			return user_name;
		}


		public void setUser_name(String user_name) {
			this.user_name = user_name;
		}


		public String getGiven_name() {
			return given_name;
		}


		public void setGiven_name(String given_name) {
			this.given_name = given_name;
		}


		public String getFamily_name() {
			return family_name;
		}


		public void setFamily_name(String family_name) {
			this.family_name = family_name;
		}
	}

