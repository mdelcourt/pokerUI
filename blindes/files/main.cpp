#ifdef __cplusplus
    #include <cstdlib>
#else
    #include <stdlib.h>
#endif

#include "SDL.h"
#include "SDL/SDL_ttf.h"
#include "SDL/SDL_image.h"
#include <SDL_image.h>

#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
using namespace std;


const int entrees_tableau=10000;
string configFile="blindes.conf";


SDL_Color noir={0,0,0};
SDL_Color rouge={255,0,0};


class timer{
public:
    int taille_tableau;
    int temps_total;
    int minute;
    int seconde;
    int init;
    bool pause;
    bool TIME;
    bool changer_niveau_plus;
    bool changer_niveau_moins;
    int choice_time;
    int time_debut;
    int duree_time;
    string *fichier_blindes;
    int niveau;
    string small_blind;
    string big_blind;
    string ante;
    int short_pause;
    
    SDL_Surface* screen;
    SDL_Surface *texte;
    SDL_Surface *image;
    SDL_Rect pos_image;
    
    SDL_Rect pos_texte;
    TTF_Font *police;
    Uint32 blanc;
    
    int res_x;
    int res_y;
    bool center;
    int font_size;
    bool img;
    string img_name;
    float img_width;

    timer(int min, int sec);
    void new_level();
    void load();
    void call_TIME();
    void start_pause();
    void stop_pause();
    void afficher();
    string gettime();
    string gettime_time();
    void loadConfig();
};

timer::timer(int min,int sec){
  
    loadConfig();
    choice_time=SDL_GetTicks();
    changer_niveau_moins=0;
    changer_niveau_plus=0;
    duree_time=60;
    TIME=false;
    screen = SDL_SetVideoMode(res_x, res_y, 16,SDL_HWSURFACE|SDL_DOUBLEBUF);
    pause=true;
    blanc=SDL_MapRGB(screen->format,255,255,255);

    police = TTF_OpenFont("jeu.ttf", font_size);
    pos_texte.x=10;
    pos_texte.y=10;

    temps_total=60*min+sec;
    niveau=0;
    init=SDL_GetTicks();

    load();
    afficher();
}

void timer::loadConfig(){
  res_x=800;
  res_y=600;
  font_size=50;
  img=false;
  ifstream is(configFile.c_str(),std::ios::in);
  if(!is) {
	  cout << "Waring: File \""<<configFile<<"\" doesn't exist. Using default values"<<endl;
    
  }
  char buf[255];
  string Parameter, Value;
  char equal;
  while(!is.eof() && !is.fail()) {
	  is>>Parameter;
	  if(Parameter[0]=='#'){
		  is.getline(buf,255);
		  continue;
	  }
	  is >> equal >> Value;
	  is.getline(buf,255);
	  if(equal!='=') {
		  cout << "Error: Syntax error for parameter "<<Parameter<<endl;
		  continue;
	  }
	  if(Parameter=="RES_X"){
		  res_x=atoi(Value.c_str());
		  continue;
	  }
	  if(Parameter=="RES_Y"){
		  res_y=atoi(Value.c_str());
		  continue;
	  }
	  if(Parameter=="FONT_SIZE"){
		  font_size=atoi(Value.c_str());
		  continue;	    
	  }
	  if(Parameter=="IMAGE"){
		  img_name=Value;
		  img=true;
		  continue;	    
	  }
	  if(Parameter=="SHORT_PAUSE"){
		  short_pause=atoi(Value.c_str());
		  continue;
	  }
	  if(Parameter=="IMAGE_WIDTH"){
		  img_width=atof(Value.c_str());
		  continue;	    
	  }

  }
}


void timer::load(){    
    fstream fichier("blindes.txt");
    fichier_blindes = new string [entrees_tableau];

    for(int i=0; i<100;i++){
        getline(fichier,fichier_blindes[i]);
        //cout<<fichier_blindes[i]<<endl;
        if (fichier_blindes[i]=="END"){taille_tableau=i; break;}
        if(i==99)cerr<<"FICHIER DE BLINDES TROP LONG"<<endl;
    }
    fichier.close();
    new_level();
}

void timer::new_level(){
    cout<<"LES BLIIIIINDES VIENNENT DE MONTEEEER"<<endl;
    system("cvlc levelup.ogg --no-loop&");
    if (niveau==taille_tableau){niveau--; cout<<"Dernier niveau de blindes"<<endl;}
    int endroit=fichier_blindes[niveau].find("SB-",0)+3;
    small_blind=fichier_blindes[niveau].substr(endroit,fichier_blindes[niveau].find(" ",endroit)-endroit);
    endroit=fichier_blindes[niveau].find("BB-",0)+3;
    big_blind=fichier_blindes[niveau].substr(endroit,fichier_blindes[niveau].find(" ",endroit)-endroit);
    endroit=fichier_blindes[niveau].find("A-",0)+2;
    ante=fichier_blindes[niveau].substr(endroit,fichier_blindes[niveau].find(" ",endroit)-endroit);
    endroit=fichier_blindes[niveau].find("T-",0)+2;
    string temps_string=fichier_blindes[niveau].substr(endroit,fichier_blindes[niveau].find(" ",endroit)-endroit);

    temps_total=0;
    for(int i=0; i<temps_string.size();i++){
        temps_total+=pow(10,(temps_string.size()-i-1))*((int)temps_string[i]-'0');
    }
    temps_total*=60;
    niveau++;
    init=SDL_GetTicks();
    //cout<<"Temps total:"<<temps_total<<endl;

}

void timer::start_pause(){
    pause=true;
    //cout<<"avt= "<<temps_total<<endl;
    temps_total-=(SDL_GetTicks()-init)/1000;
    //cout<<"temps total après: "<<temps_total<<endl;
    SDL_Delay(100);
}

void timer::stop_pause(){

    pause=false;
    init=SDL_GetTicks();
    //cout<<"Fin de la pause"<<endl;
    SDL_Delay(100);
}

void timer::afficher(){
    int i=0;
    bool keyIsDown=false;
    while (true){
        SDL_Event event;
	while(SDL_PollEvent(&event) && event.type==SDL_MOUSEMOTION){continue;}
        if(event.type==SDL_QUIT) exit(1);
	if(event.type==SDL_KEYUP){
	  keyIsDown=false;
	}
        if(event.type==SDL_KEYDOWN and not keyIsDown){
	    keyIsDown=true;
            if(event.key.keysym.sym==SDLK_SPACE && pause){stop_pause(); SDL_Delay(100);}
            else if(event.key.keysym.sym==SDLK_i){system("cvlc  intro.mp3 --no-loop&");SDL_Delay(100); }
            else if(event.key.keysym.sym==SDLK_e){system("cvlc  ept_opening.mp3 --no-loop&");SDL_Delay(100); }
            else if(event.key.keysym.sym==SDLK_g){system("cvlc  gogole.mp3 --no-loop&");SDL_Delay(100); }
            else if(event.key.keysym.sym==SDLK_SPACE){start_pause(); }
            else if(event.key.keysym.sym==SDLK_t){ if(!TIME) call_TIME(); else {TIME=false; SDL_Delay(100);} }
            else if (event.key.keysym.sym==SDLK_RIGHT){
                if(!changer_niveau_plus){cout<<"Réappuyez pour changer de niveau"<<endl; changer_niveau_plus=true; SDL_Delay(100);choice_time=SDL_GetTicks();}
                else{
                    changer_niveau_plus=false;
//                     SDL_Delay(500);
                    new_level();
                }
            }
            else if (event.key.keysym.sym==SDLK_LEFT){
                if(!changer_niveau_moins){cout<<"Réappuyez pour changer de niveau"<<endl; changer_niveau_moins=true; SDL_Delay(500); choice_time=SDL_GetTicks();}
                else{

                    changer_niveau_moins=false;
//                     SDL_Delay(500);
                    niveau-=2;
                    if(niveau<1) niveau=0;
                    new_level();
                }
            }
        }
        else{
	  if ((SDL_GetTicks()-choice_time)>2000&&(changer_niveau_moins||changer_niveau_plus)){
	      cout<<"Time out"<<endl;
	      changer_niveau_moins=false;
	      changer_niveau_plus=false;
	  }

	  SDL_FillRect(screen,NULL,blanc);
	  
	  //Afficher logos
  // 	cout<<"Affichage de logos. i="<<i<<endl;
  // 	if (i==0){
  // 	  image=IMG_Load(img_name.c_str());
  // 	}
	  if(i%10==0){
	    if (i>0){
	      SDL_FreeSurface(image);
	    }
	    image=IMG_Load(img_name.c_str());
	  }
	  pos_image.x=0;
	  pos_image.y=200;
  // 	pos_image.width=200;
	  SDL_BlitSurface(image, NULL, screen, &pos_image);

	  texte=TTF_RenderText_Blended(police,gettime().c_str(),noir);
	  pos_texte.y=10+texte->h;
	  pos_texte.x=10;

	  SDL_BlitSurface(texte,NULL,screen,&pos_texte);
	  SDL_FreeSurface(texte);
	  pos_texte.x+=texte->w;
	  string texte_a_afficher;
	  texte_a_afficher+=" SB: "+small_blind+" BB: "+big_blind;
	  if (ante[0]-'0'>0) texte_a_afficher+=" Ante: "+ante;
	  pos_texte.x=0;
	  pos_texte.y=0;
	  texte=TTF_RenderText_Blended(police,texte_a_afficher.c_str(),noir);
	  SDL_BlitSurface(texte,NULL,screen,&pos_texte);
	  SDL_FreeSurface(texte);

	  if(TIME){
	      pos_texte.y+=110;
	      texte=TTF_RenderText_Blended(police,"TIME",rouge);
	      pos_texte.x=(screen->w)/2-(texte->w)/2;
	      SDL_BlitSurface(texte,NULL,screen,&pos_texte);
	      SDL_FreeSurface(texte);
	      if ((SDL_GetTicks()-time_debut)<=duree_time*1000)texte=TTF_RenderText_Blended(police,gettime_time().c_str(),rouge);
	      else if((SDL_GetTicks()-time_debut)>(duree_time+10)*1000) {TIME=false; continue;}
	      else texte=TTF_RenderText_Blended(police,"FOLD HAHAHA",rouge);

	      pos_texte.x=(screen->w)/2-(texte->w)/2;
	      pos_texte.y+=texte->h+5;
	      SDL_BlitSurface(texte,NULL,screen,&pos_texte);
	      SDL_FreeSurface(texte);
	      pos_texte.x=10;
	      pos_texte.y-=110+2*(texte->h+5);
	  }
	  
	  
	  SDL_Flip(screen);
	  SDL_Delay(short_pause);
	  i++;
	}
//         if(event.type!=SDL_MOUSEMOTION)SDL_Delay(short_pause);
    }
}

string timer::gettime(){
    if (temps_total-(SDL_GetTicks()-init)/1000>temps_total&& !pause) new_level();
    //cout<<temps_total-temps_total-(SDL_GetTicks()-init)/1000<<endl;
     ostringstream temp;
    if(!pause) seconde=temps_total-(SDL_GetTicks()-init)/1000;
    else seconde=temps_total;
    minute=seconde/60;
    if (minute<10) temp<<"0"<<minute;
    else temp<<minute;
    if (seconde%60<10)     temp<<":0"<<seconde%60;
    else    temp<<":"<<seconde%60;
    if(pause) temp<<"  PAUSE";
    return temp.str();
}


string timer::gettime_time(){
    ostringstream temp;
    seconde=duree_time-(SDL_GetTicks()-time_debut)/1000;
    temp<<seconde<<"!!!";
    return temp.str();
}



void timer::call_TIME(){
    TIME=true;
    //cout<<"TIIIIIIIIIIIIIIIIIIME"<<TIME<<endl;
    time_debut=SDL_GetTicks();
    SDL_Delay(200);
}

int main ( int argc, char** argv )
{

//     cout<<pow(7,(double)1/17)<<endl;

    SDL_Init( SDL_INIT_VIDEO );
    TTF_Init();
    atexit(SDL_Quit);

    timer ma_blinde(10,0);
}
