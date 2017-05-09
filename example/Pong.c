// Michael O'Malley
// cse20211
// This program will recreate the classic game pong

#include <stdio.h>
#include "gfx5.h"
#include <math.h>
#include <string.h>

// Prototypes
void menu(void);
int dmenu(void);
void winmenu(char*, char*, char);
void countdown(int, char*, char*, double x);
int drwfield(char*, char*, double);
void comp(double, double*, double, int, int*);
void ball(double*, double*, double*, double*, double*, double*, double*, int);
void oneplayer(char*, char*, char, double, double, double, double, double, double, double, double, double, int, int, int);
void twoplayer(char*, char*, char, double, double, double, double, double, double, double, double, double, int, int, int);
void practice(char*, char*, char, double, double, double, double, double, double, double, double, double, int, int, int);

int main(void)
{
	int true = 1;		// While loop truth value
	int n = 0;			// Point scored indicator
	int t = 4;			// Speed variable
	int press;			// Button release indicator
	time_t s;						// Establish time variable
	srand((unsigned) time(&s));		// Set seed for rand()
	double x = 500;		// Ball x coordinate
	double y = 300;		// Ball y coordinate
	double x1 = 50;		// Right bar x coordinate
	double y1 = 300;	// Right bar y coordinate
	double x2 = 950;	// Left bar x coordinate
	double y2 = 300;	// Left bar y coordinate
	double deg = (rand() % 46)+15;		// Random number from 0 to 360
	double dir = (rand() % 2)*M_PI;		// Random direction
	double rad = ((deg*M_PI)/180)+dir;	// Convert random degree angle to radian angle
	char c;					// Input variable
	char score1[] = "0";	// Score 1 string
	char score2[] = "0";	// Score 2 string
	
	gfx_open(1000, 600, "PONG");
	gfx_clear();
	menu();

	while(true){
		usleep(8000);
		if(gfx_event_waiting()){			// Wait for input
			press = gfx_event_waiting();	// Set 'press' to indicate key press or key release
			c = gfx_wait();					// Set 'c' equal to key press
			switch(c){						// Perform specific function according to 'c'
				case '1':
					oneplayer(score1, score2, c, x, y, x1, y1, x2, y2, deg, dir, rad, t, n, press);
					break;
				case '2':
					twoplayer(score1, score2, c, x, y, x1, y1, x2, y2, deg, dir, rad, t, n, press);
					break;		
				case '3':	
					practice(score1, score2, c, x, y, x1, y1, x2, y2, deg, dir, rad, t, n, press);	
					break;
				case 'q':		// If 'q' is pressed, exit the program
					true = 0;
					break;
					
			}		
		}
	}	
}		

void menu(void){			// This function displays a menu of game options
	gfx_color(0,255,0);
	gfx_text(498, 150, "PONG");
	gfx_text(275, 250, "1. Single Player: Play against the computer of varying difficulty. Use 'W' to move");
	gfx_text(385, 265, "up and 'S' to move down. First to ten wins!");
	gfx_text(275, 300, "2. Two Player: Play against a friend! Player 1 will use 'W' to move up and 'S' to move down.");
	gfx_text(365, 315, "Player 2 will use 'I' to move up and 'K' to move down. First to ten wins!");
	gfx_text(275, 350, "3. Practice Mode: Practice against a wall for as long as you want! Press 'D' to speed");
	gfx_text(382, 365, "the ball up, 'A' to slow it down, and 'Q' to quit the mode.");
	gfx_text(460, 450, "Press 'Q' to quit.");
}	

int dmenu(void){	// This function displays a difficulty menu and returns a value for the chosen difficulty
	char c;
	gfx_clear();
	gfx_color(0,255,0);
	gfx_text(468, 225, "SET DIFFICULTY");
	gfx_text(472, 275, "1. Beginner");
	gfx_text(472, 300, "2. Intermedate");
	gfx_text(472, 325, "3. Advcanced");
	gfx_text(472, 350, "4. Impossible");
	while(1){
		usleep(8000);
		if(gfx_event_waiting()){
			c = gfx_wait();
			switch(c){			// Switch case that returns the entered value as an integer
				case '1':
					return 1;
					break;
				case '2':
					return 2;
					break;
				case '3':
					return 3;
					break;
				case '4':
					return 4;
					break;
			}
		}
	}
}

void winmenu(char *score1, char *score2, char c){	// This function displays a menu when a game is finished listing the
	int press;										// winner and the final score
	gfx_clear();
	gfx_color(0,255,0);
	if(!strcmp(score1, "10")){					
		gfx_text(468, 225, "Player 1 wins!");	// If the right bar wins, say 'Player 1 wins'
	}
	else if(!strcmp(score2, "10") && c == '2'){	// If the left bar wins in 2 player mode, say 'Player 2 wins'
		gfx_text(468, 225, "Player 2 wins!");
	}
	else if(!strcmp(score2, "10") && c == '1'){	// If the left bar wins in 1 player mode, say 'Computer wins'
		gfx_text(468, 225, "Computer wins!");
	}
	gfx_text(472, 275, "Final Score:");
	strcat(score1, " - ");					// Add a dash after Player 1's score
	strcat(score1, score2);					// Combine Player 1 score and Player 2 score into one string
	gfx_text(490, 325, score1);
	gfx_text(455, 400, "Press 'Q' to return");
	while(1){
		usleep(8000);
		if(gfx_event_waiting()){			// In order to exit the screen and return to the menu, the user must hit 'q'
			press = gfx_event_waiting();
			c = gfx_wait();
			if(c == 'q' && press == 2){
				gfx_clear();
				return;
			}
		}
	}
}

int drwfield(char *score1, char *score2, double x){	// This function draws the field of play with varying scores. It returns
	int i = 0;	// Accumulator							// a variable that indicates a point was scored
	int m = 0;	// Increment variable for dashed line
	int n;		// Point scored integer
	gfx_color(255,255,255);
	gfx_rectangle(10, 10, 980, 580);
	while(i <= 20){						// Center line while loop	
		gfx_line(500, m+15, 500, m+45);	// Draw dash marks on y-axis
		m = i*30;
		i += 2;	// Increment i
	}
	gfx_text(470, 25, score1);
	gfx_text(525, 25, score2);
	if(x+5 <= -5){
		n = atoi(score2);			// Convert number string to integer
		n++;						// Increment integer
		sprintf(score2, "%d", n); 	// Convert integer back to string
		return 1;
	}
	else if(x-5 >= 1005){
		n = atoi(score1);			
		n++;					
		sprintf(score1, "%d", n);
		return 1;
	}
	else{
		return 0;
	}
}

// This function provides the computer player with location variables for the deflecting bar. The bar does this by 
// following the vertical motion of the bar at a slower speed. Different difficulties change bar speed and ball speed.
void comp(double y, double *y2, double rad, int d, int *t){ 
	if(cos(rad) > 0){
		if(d == 1){			// Slow ball with slow following									
			*t = 3;
			if((y > *y2 && sin(rad) > 0) || (y < *y2 && sin(rad) < 0)){
				*y2 += (*t*sin(rad))/1.4;
			}
			else if((y > *y2 && sin(rad) < 0) || (y < *y2 && sin(rad) > 0)){
				*y2 -= (*t*sin(rad))/1.4;
			}
		}
		else if(d == 2){	//  Average speed ball with somewhat slow following
			*t = 4;
			if((y > *y2 && sin(rad) > 0) || (y < *y2 && sin(rad) < 0)){
				*y2 += (*t*sin(rad))/1.3;
			}
			else if((y > *y2 && sin(rad) < 0) || (y < *y2 && sin(rad) > 0)){
				*y2 -= (*t*sin(rad))/1.3;
			}
		}
		else if(d == 3){	// Quick ball with quick following
			*t = 5;
			if((y > *y2 && sin(rad) > 0) || (y < *y2 && sin(rad) < 0)){
				*y2 += (*t*sin(rad))/1.2;
			}
			else if((y > *y2 && sin(rad) < 0) || (y < *y2 && sin(rad) > 0)){
				*y2 -= (*t*sin(rad))/1.2;
			}
		}
		else if(d == 4){	// Fast ball with fast following
			*t = 6;
			if((y > *y2 && sin(rad) > 0) || (y < *y2 && sin(rad) < 0)){
				*y2 += (*t*sin(rad))/1.1;
			}
			else if((y > *y2 && sin(rad) < 0) || (y < *y2 && sin(rad) > 0)){
				*y2 -= (*t*sin(rad))/1.1;
			}
		}
	}
	if(*y2 <= 61){		// If statements that keep the bar from going to high or too low
		*y2 = 61;
	}
	if(*y2 >= 539){
		*y2 = 539;
	}
}

void ball(double *rad, double *x, double *y, double *x1, double *y1, double *x2, double *y2, int t){
	int n;
	if(*x >= 15 && *x <= 985){
		gfx_fill_circle(*x, *y, 5);		// Draw a circle at x, y with radius r
	}
	gfx_flush;	
	*x += t*cos(*rad);		// Change x position with random angle for next animation
	*y += t*sin(*rad);		// Change y position with random angle for next animation
	if(*y2 != 0){
		if((*x+5 >= *x2-5 && *x+5 <= *x2-(5-t) && *y <= *y2+55 && *y >= *y2-55) 		// Detects if ball hit bar 
			|| (*x-5 <= *x1+5 && *x-5 >= *x1+(5-t) && *y <= *y1+55 && *y >= *y1-55)){
			*rad = M_PI - *rad;	
		}
	}
	else{
		if(*x+5 >= 995 || (*x-5 <= *x1+5 && *x-5 >= *x1+(5-t) && *y <= *y1+55 && *y >= *y1-55)){ // Detects if ball hit bar 
			*rad = M_PI - *rad;																	 // or wall
		}
	}
	if(*y+5 >= 590 || *y-5 <= 10){
		*rad = - *rad;		
	}
}

// This function allows the user to play against a computer player
void oneplayer(char *score1, char *score2, char c, double x, double y, double x1, double y1, double x2, double y2, double deg, double dir, double rad, int t, int n, int press){
	int d;
	time_t s;						// Establish time variable
	srand((unsigned) time(&s));		// Set seed for rand()
	if(press == 2){					// Keeps the program from skipping the difficulty menu
		d = dmenu();				// Difficulty menu
		sprintf(score1, "%d", 0);	// Reset scores
		sprintf(score2, "%d", 0);
		while(1){
			gfx_clear();
			n = drwfield(score1, score2, x);			// Draw the field with current scores
			ball(&rad, &x, &y, &x1, &y1, &x2, &y2, t);	// Draw next iteration of the ball
			if(n == 1){		// If a point was scored, reset the ball at a random angle
				x = 500;
				y = 300;
				deg = (rand() % 46)+15;	
				dir = (rand() % 2)*M_PI;
				rad = ((deg*M_PI)/180)+dir;
				n = 0;
			}
			if(!strcmp(score1, "10") || !strcmp(score2, "10")){	// If someone won, display the win menu and exit mode
				winmenu(score1, score2, '1');
				menu();
				return;
			}
			gfx_color(255,0,0);
			gfx_fill_rectangle(x1-5, y1-50, 10, 100);	// Draw red right bar
			gfx_color(255,255,0);
			comp(y, &y2, rad, d, &t);					// Calculate computer player position
			gfx_fill_rectangle(x2-5, y2-50, 10, 100);	// Draw yellow computer player
			usleep(8000);				
			if(gfx_event_waiting()){
				press = gfx_event_waiting();
				c = gfx_wait();
				switch(c){
					case 'w':
						y1 -= 15;		// 'w' and 's' add or subtract 15 units from the right bar
						if(y1 <= 61){	// If statements that keep the bar from going to high or too low
							y1 = 61;
						}
						break;
					case 's':
						y1 += 15;
						if(y1 >= 539){
							y1 = 539;
						}
						break;
					case 'q':			// If 'q' is pressed, quit the program
						if(press == 2){
							gfx_clear();
							menu();
							return;
						}
						break;
				}
			}
		}
	}
}

// This function allows the user to play against a second player
void twoplayer(char *score1, char *score2, char c, double x, double y, double x1, double y1, double x2, double y2, double 	deg, double dir, double rad, int t, int n, int press){
	time_t s;						// Establish time variable
	srand((unsigned) time(&s));		// Set seed for rand()
	sprintf(score1, "%d", 0);
	sprintf(score2, "%d", 0);
	while(1){					// Comments for the next several lines are the same as those above in the oneplayer function
		gfx_clear();
		n = drwfield(score1, score2, x);
		ball(&rad, &x, &y, &x1, &y1, &x2, &y2, t);
		if(n == 1){
			x = 500;
			y = 300;
			deg = (rand() % 46)+15;	
			dir = (rand() % 2)*M_PI;
			rad = ((deg*M_PI)/180)+dir;
			n = 0;
		}
		if(!strcmp(score1, "10") || !strcmp(score2, "10")){
			winmenu(score1, score2, '2');
			menu();
			return;
		}
		gfx_color(255,0,0);
		gfx_fill_rectangle(x1-5, y1-50, 10, 100);	// Draw right bar
		gfx_color(0,0,255);
		gfx_fill_rectangle(x2-5, y2-50, 10, 100);	// Draw left bar
		usleep(8000);				
		if(gfx_event_waiting()){	// Wait for input
			press = gfx_event_waiting();
			c = gfx_wait();
			switch(c){
				case 'w':				// 'w' and 's' add or subtract 15 units from the right bar
					if(cos(rad) < 0){	// If the ball is moving towards this bar, it can move.
						y1 -= 15;
						if(y1 <= 61){
							y1 = 61;
						}
					}
					break;
				case 's':
					if(cos(rad) < 0){	// If the ball is moving towards this bar, it can move.
						y1 += 15;
						if(y1 >= 539){
							y1 = 539;
						}
					}
					break;
				case 'i':				// 'i' and 'j' add or subtract 15 units from the right bar
					if(cos(rad) > 0){	// If the ball is moving towards this bar, it can move.
						y2 -= 15;
						if(y2 <= 61){
							y2 = 61;
						}
					}
					break;
				case 'k':
					if(cos(rad) > 0){	// If the ball is moving towards this bar, it can move.
						y2 += 15;
						if(y2 >= 539){
							y2 = 539;
						}
					}
					break;
				case 'q':	// If 'q' is pressed, quit the game mode
					if(press == 2){
						gfx_clear();
						menu();
						return;
					}
					break;
			}
		}				
	}			
}

// This function allows the user to practice their skills against a wall
void practice(char *score1, char *score2, char c, double x, double y, double x1, double y1, double x2, double y2, double deg, double dir, double rad, int t, int n, int press){
	time_t s;			// Establish time variable
	srand((unsigned) time(&s));		// Set seed for rand()
	y2 = 0;							// Indicate that there is no second player and to detect the wall, not a bar
	sprintf(score1, "%d", 0);
	sprintf(score2, "%d", 0);	
	while(1){
		gfx_clear();
		n = drwfield("\0", score2, x);
		ball(&rad, &x, &y, &x1, &y1, &x2, &y2, t);
		if(n == 1){
			x = 500;
			y = 300;
			deg = (rand() % 46)+15;	
			dir = (rand() % 2)*M_PI;
			rad = ((deg*M_PI)/180)+dir;
			n = 0;
		}
		gfx_color(255,0,0);
		gfx_fill_rectangle(x1-5, y1-50, 10, 100);
		gfx_color(255,0,0);
		usleep(8000);				
		if(gfx_event_waiting()){	// Wait for input
			press = gfx_event_waiting();
			c = gfx_wait();
			switch(c){
				case 'w':			// 'w' and 's' add or subtract 15 units from the right bar
					y1 -= 15;
					if(y1 <= 61){
						y1 = 61;
					}
					break;
				case 's':
					y1 += 15;
					if(y1 >= 539){
						y1 = 539;
					}
					break;
				case 'd':			// 'd' and 'a' add or subtract to the speed of the ball
					if(press == 2){
						t++;
						if(t > 7){	// The ball can't get faster than a given value
						 t = 7;
						}
					}
					break;
				case 'a':
					if(press == 2){
						t--;
						if(t < 1){	// The ball can't get slower than a given value
						 t = 1;
						}
					}
					break;
				case 'q':
					if(press == 2){	// If 'q' is pressed, quit the mode
						gfx_clear();
						menu();
						return;
					}
					break;
			}
		}
	}
}
