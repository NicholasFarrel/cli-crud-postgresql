-- Tabela Escalador
INSERT INTO Escalador VALUES (31, 'Calango');
INSERT INTO Escalador VALUES (32, 'Beznos');
INSERT INTO Escalador VALUES (33, 'Nicholas');
INSERT INTO Escalador VALUES (34, 'Bocheca');
INSERT INTO Escalador VALUES (35, 'Claudinho');

-- Tabela Setor
INSERT INTO Setor VALUES (11, '-22.9519, -43.2105');
INSERT INTO Setor VALUES (12, '-12.9822, -38.4813');
INSERT INTO Setor VALUES (13, '-20.3199, -40.3382');
INSERT INTO Setor VALUES (14, '-27.5954, -48.5480');
INSERT INTO Setor VALUES (15, '-3.1190, -60.0217');

-- Tabela EstiloVia
INSERT INTO EstiloVia VALUES (1, 'Sport');
INSERT INTO EstiloVia VALUES (2, 'Boulder');
INSERT INTO EstiloVia VALUES (3, 'Trad');


-- Tabela Via
INSERT INTO Via VALUES (41, 'Pedrita', 11, 1);
INSERT INTO Via VALUES (42, 'Epitáfios', 12, 1);
INSERT INTO Via VALUES (43, 'Migalhas', 13, 1);
INSERT INTO Via VALUES (44, 'Bambam', 14, 1);
INSERT INTO Via VALUES (45, 'Omalaka', 15, 2);

-- Tabela Ascensao
INSERT INTO Ascensao VALUES (21, '2004-01-15', 1, 41, 31);
INSERT INTO Ascensao VALUES (22, '2004-01-16', 2, 42, 31);
INSERT INTO Ascensao VALUES (23, '2004-01-17', 3, 43, 33);
INSERT INTO Ascensao VALUES (24, '2004-01-18', 4, 44, 34);
INSERT INTO Ascensao VALUES (25, '2004-01-19', 5, 45, 34);

-- Tabela EscaladorSegueSetor
INSERT INTO EscaladorSegueSetor VALUES (31, 11);
INSERT INTO EscaladorSegueSetor VALUES (31, 12);
INSERT INTO EscaladorSegueSetor VALUES (31, 13);
INSERT INTO EscaladorSegueSetor VALUES (35, 14);
INSERT INTO EscaladorSegueSetor VALUES (34, 14);

-- Tabela EscaladorSegueEscalador
INSERT INTO EscaladorSegueEscalador VALUES (31, 32);
INSERT INTO EscaladorSegueEscalador VALUES (31, 33);
INSERT INTO EscaladorSegueEscalador VALUES (31, 34);
INSERT INTO EscaladorSegueEscalador VALUES (33, 34);
INSERT INTO EscaladorSegueEscalador VALUES (33, 32);
INSERT INTO EscaladorSegueEscalador VALUES (34, 31);


--------- Inserts para o mistério ficar mais interessante ---------------
INSERT INTO Via VALUES (46, 'TicTic Nervoso', 11, 1);

-- Vias de média alta - bochecha avalia com 1
INSERT INTO Via VALUES (47, 'Sossego', 12, 2);
INSERT INTO Via VALUES (48, 'Caminho Suave', 13, 1);

INSERT INTO Ascensao VALUES (32, '2004-01-15', 5, 47, 31); -- Calango
INSERT INTO Ascensao VALUES (33, '2004-01-16', 4, 47, 33); -- Nicholas

INSERT INTO Ascensao VALUES (34, '2004-01-15', 5, 48, 32); -- Beznos
INSERT INTO Ascensao VALUES (35, '2004-01-16', 5, 48, 33); -- Nicholas

INSERT INTO Ascensao VALUES (36, '2004-01-23', 1, 47, 34); -- Bochecha
INSERT INTO Ascensao VALUES (37, '2004-01-23', 1, 48, 34); -- Bochecha

-- Vias de média baixa - bochecha avalia com 5
INSERT INTO Via VALUES (49, 'Areia Movediça', 14, 3);
INSERT INTO Via VALUES (50, 'Chorume', 15, 2);

INSERT INTO Ascensao VALUES (38, '2004-01-15', 2, 49, 31); -- Calango
INSERT INTO Ascensao VALUES (39, '2004-01-16', 1, 49, 32); -- Beznos

INSERT INTO Ascensao VALUES (40, '2004-01-15', 1, 50, 31); -- Calango
INSERT INTO Ascensao VALUES (41, '2004-01-16', 2, 50, 33); -- Nicholas

INSERT INTO Ascensao VALUES (42, '2004-01-23', 5, 49, 34); -- Bochecha
INSERT INTO Ascensao VALUES (43, '2004-01-23', 5, 50, 34); -- Bochecha


INSERT INTO Ascensao VALUES (44, '2004-01-14', 5, 41, 31); -- Calango
INSERT INTO Ascensao VALUES (45, '2004-01-13', 5, 41, 33); -- Nicholas

INSERT INTO Ascensao VALUES (46, '2004-01-14', 5, 47, 32); -- Beznos
INSERT INTO Ascensao VALUES (47, '2004-01-14', 5, 48, 35); -- Claudinho

INSERT INTO Ascensao VALUES (48, '2004-01-14', 1, 49, 33); -- Nicholas
INSERT INTO Ascensao VALUES (49, '2004-01-14', 2, 50, 32); -- Beznos


INSERT INTO Ascensao VALUES (50, '2004-01-25', 5, 47, 35); -- Claudinho
INSERT INTO Ascensao VALUES (51, '2004-01-25', 5, 41, 35); -- Claudinho



INSERT INTO Ascensao VALUES (52, '2004-01-25', 1, 49, 35); -- Claudinho
INSERT INTO Ascensao VALUES (53, '2004-01-25', 1, 50, 35); -- Claudinho



-- Vias que o claudinho mandou com nota 1
INSERT INTO Ascensao VALUES (26, '2004-01-20', 1, 41, 35); -- Pedrita
INSERT INTO Ascensao VALUES (27, '2004-01-21', 1, 43, 35); -- Migalhas
INSERT INTO Ascensao VALUES (31, '2004-01-22', 1, 46, 35); -- Tic tic 

-- Primeira lista de suspeitos
INSERT INTO Ascensao VALUES (28, '2004-01-10', 5, 41, 32); -- Beznos foi o primeiro na Pedrita
INSERT INTO Ascensao VALUES (29, '2004-01-12', 4, 43, 33); -- Nicholas foi o primeiro na Migalhas
INSERT INTO Ascensao VALUES (30, '2004-01-11', 5, 46, 34); -- Bochecha foi o primeiro na Tictic


-- Segunda lista de suspeitos (únicos seguidores de setor)
INSERT INTO EscaladorSegueSetor VALUES (32, 11); -- Beznos
INSERT INTO EscaladorSegueSetor VALUES (34, 11); -- Bochecha


INSERT INTO EscaladorSegueSetor VALUES (31, 14); -- já existe
INSERT INTO EscaladorSegueSetor VALUES (34, 15); -- já existe
INSERT INTO EscaladorSegueSetor VALUES (33, 12); -- Nicholas segue outro setor
