from incibe import INCIBEScraper
import constants

# Crea un objeto 
scraper = INCIBEScraper();

# Llama a la función principal
scraper.scrape();

# Guarda los resultados
scraper.save2json(constants.OUTPUT_FILENAME);
