import json
from os import system
msg = '''
   ********        **        ****     ****   ******** 
  **//////**      ****      /**/**   **/**  /**/////  
 **      //      **//**     /**//** ** /**  /**       
/**             **  //**    /** //***  /**  /*******  
/**    *****   **********   /**  //*   /**  /**////   
//**  ////**  /**//////**   /**   /    /**  /**       
 //********   /**     /**   /**        /**  /******** 
  ////////    //      //    //         //   ////////  

                 *******     **      **   ********   *******  
                **/////**   /**     /**  /**/////   /**////** 
               **     //**  /**     /**  /**        /**   /** 
              /**      /**  //**    **   /*******   /*******  
              /**      /**   //**  **    /**////    /**///**  
              //**     **     //****     /**        /**  //** 
               //*******       //**      /********  /**   //**
                ///////         //       ////////   //     // 
'''     

def display_end(score):
    system('clear')
    alias = input('Enter your Alias : ')
    di = {}
    with open("scoreboard.json","r") as oi:
        di = json.load(oi)
    di[alias] = score
    with open("scoreboard.json","w") as oi:
        oi.write(json.dumps(di,indent=4))
    system('clear')
    print(msg)
    for i in di.keys():
        print(i,"\t\t===> ",di[i])


