#include "header.h"
class me {
public:
bios *io = new bios;

;
std::string life = "yes";
std::string name;
std::string panda(){
this->name = "Panda";
return this->name;
}
};
int main(int argc,char*argv[]){
me* new_me = new me();
;
std::string life = new_me->life;
;
std::string name = new_me->panda();
;
new_me->io->print(name);
new_me->io->print(life);
}
