#include <stdio.h>





int main(void) {

    FILE *fpr;
    FILE *fpw;


    unsigned char buffer4[4];
    unsigned char buffer2[2];

    fpr = fopen("Free_Test_Data_500KB_WAV.wav", "r");

    if (fpr == NULL) {
        printf("Could not open file");
    }

    fread(buffer2, 1024, 1, fpr);

    return 0;
}



