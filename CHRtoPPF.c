#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const unsigned char Raquet_PPFHeader[8] = {
    0x50,
    0x50,
    0x46,
    0x76,
    0x01,
    0x00,
    0x00,
    0x00
};

int main(int argc, char** argv) {

    if (argc <= 1) {
        printf("No CHR files submitted.\n");
        return 1;
    }

    for (int i = 1; i < argc; ++i) {
       
        char* newname = malloc(sizeof(char) * (strlen(argv[i]) + 4));
        strcat(newname, argv[i]);
        strcat(newname, ".ppf");

        printf("%s\n", newname);

        FILE* file = fopen(newname, "ab+");

        if (file == NULL) {
            puts("Error in creating PPF file");
            return 1;
        }
 
        FILE* chrfile = fopen(argv[i], "rb");
        fseek(chrfile, 0L, SEEK_END);
        int chrfile_length = ftell(chrfile);
        char chrdata[chrfile_length];
        rewind(chrfile);
        fread(chrdata, sizeof(char), chrfile_length, chrfile);

        char ppfdata[8 + chrfile_length];
        
        for (int i = 0; i < 8; i++) {
            ppfdata[i] = Raquet_PPFHeader[i];
        }

        for (int i = 8; i < chrfile_length; i++) {
            ppfdata[i] = chrdata[i - 8];
        }

        fwrite(ppfdata, sizeof(char), chrfile_length + 8, file);

        fclose(file);

    }

    return 0;

}
