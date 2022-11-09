# WebScraperDictionary
Web scraper for 'Vocabulario de Comercio Medieval'

Make sure that the required MySQL database is available. Use the following MySQL instructions:

CREATE TABLE `dizionario`.`parola` (
  `id` MEDIUMINT(5) NOT NULL,
  `termine` VARCHAR(50) NULL,
  `definizione` MEDIUMTEXT NULL,
  `categoria` VARCHAR(50) NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `dizionario`.`citazione` (
  `documento` VARCHAR(200) NOT NULL,
  `parola` MEDIUMINT(5) NOT NULL,
  `testo` MEDIUMTEXT NULL,
  PRIMARY KEY (`documento`, `parola`),
  INDEX `parola_idx` (`parola` ASC) VISIBLE,
  CONSTRAINT `cit_parola`
    FOREIGN KEY (`parola`)
    REFERENCES `dizionario`.`parola` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `dizionario`.`immagine` (
  `URL` VARCHAR(200) NOT NULL,
  `parola` MEDIUMINT(5) NOT NULL,
  `descrizione` TINYTEXT NULL,
  PRIMARY KEY (`URL`),
  INDEX `parola_idx` (`parola` ASC) VISIBLE,
  CONSTRAINT `imm_parola`
    FOREIGN KEY (`parola`)
    REFERENCES `dizionario`.`parola` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `dizionario`.`fonte` (
  `documento` VARCHAR(400) NOT NULL,
  `parola` MEDIUMINT(5) NOT NULL,
  `URL` VARCHAR(200) NULL,
  PRIMARY KEY (`documento`, `parola`),
  INDEX `parola_idx` (`parola` ASC) VISIBLE,
  CONSTRAINT `fon_parola`
    FOREIGN KEY (`parola`)
    REFERENCES `dizionario`.`parola` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE)
;
