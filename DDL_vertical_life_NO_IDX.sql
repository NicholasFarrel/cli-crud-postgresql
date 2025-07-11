CREATE schema VerticalLifeNoIdx;

set search_path = VerticalLifeNoIdx;

CREATE TABLE Escalador
(
  IDEscalador INT NOT NULL,
  NomeEscalador VARCHAR NOT NULL,
  PRIMARY KEY (IDEscalador)
);

CREATE TABLE Setor
(
  IDSetor INT NOT NULL,
  LocalSetor VARCHAR NOT NULL,
  PRIMARY KEY (IDSetor)
);

CREATE TABLE EstiloVia
(
  IDEstiloVia INT NOT NULL,
  NomeEstiloVia VARCHAR NOT NULL,
  PRIMARY KEY (IDEstiloVia)
);

CREATE TABLE EscaladorSegueSetor
(
  IDEscalador INT NOT NULL,
  IDSetor INT NOT NULL,
  PRIMARY KEY (IDEscalador, IDSetor),
  FOREIGN KEY (IDSetor) REFERENCES Setor(IDSetor),
  FOREIGN KEY (IDEscalador) REFERENCES Escalador(IDEscalador)
);

CREATE TABLE EscaladorSegueEscalador
(
  IDEscaladorSegue INT NOT NULL,
  IDEscaladorSeguido INT NOT NULL,
  PRIMARY KEY (IDEscaladorSegue, IDEscaladorSeguido),
  FOREIGN KEY (IDEscaladorSegue) REFERENCES Escalador(IDEscalador),
  FOREIGN KEY (IDEscaladorSeguido) REFERENCES Escalador(IDEscalador)

);

CREATE TABLE Via
(
  IDVia INT NOT NULL,
  NomeVia VARCHAR NOT NULL,
  IDSetor INT NOT NULL,
  IDEstiloVia INT NOT NULL,
  PRIMARY KEY (IDVia),
  FOREIGN KEY (IDSetor) REFERENCES Setor(IDSetor),
  FOREIGN KEY (IDEstiloVia) REFERENCES EstiloVia(IDEstiloVia)
);

CREATE TABLE Ascensao
(
  IDAscensao INT NOT NULL,
  DataAscensao DATE NOT NULL,
  NotaAscensao INT NOT NULL,
  IDVia INT NOT NULL,
  IDEscalador INT NOT NULL,
  PRIMARY KEY (IDAscensao),
  FOREIGN KEY (IDVia) REFERENCES Via(IDVia),
  FOREIGN KEY (IDEscalador) REFERENCES Escalador(IDEscalador)
);
