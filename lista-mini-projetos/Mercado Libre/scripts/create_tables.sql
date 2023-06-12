--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- SCRIPTS DDL
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Cria��o do Banco de Dados Utilizado
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

DECLARE @dbname nvarchar(128)
SET @dbname = N'BD_MERCADOLIBRE'

IF EXISTS (SELECT name FROM master.sys.databases WHERE name = @dbname)
BEGIN
	PRINT 'db exists.'
END

ELSE
BEGIN
	CREATE DATABASE BD_MERCADOLIBRE
END

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Script base para utiliza��o do Banco de Dados definido
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
/* Sempre que utilizarmos o prefixo com o nome do Banco de Dados de agora em diante, executaremos uma string SQL. Deste modo, caso seja necess�rio criar um Banco de Dados teste, basta somente alterar a vari�vel @dbname */

DECLARE @SQL NVARCHAR(128)
SET @sql = N'USE ' + QUOTENAME(@dbname)

EXEC sp_executesql @sql
GO


-- criar tabela tempor�ria como ## para n�o precisar declarar duas vezes a variavel

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Cria��o Tabelas Fato
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
/* Tabela Item - entidade onde se encontram os produtos publicados no marketplace. */
DROP TABLE IF EXISTS [dbo].FACT_ITEM;
CREATE TABLE [dbo].FACT_ITEM (
	[ITEM_ID] INT IDENTITY NOT NULL
	, [ITEM_NAME] VARCHAR(150) NOT NULL
	, [ITEM_STATE] AS IIF(ISNULL([END_DATE], '') = '', 'Active', 'Inactive')
	, [END_DATE] DATETIME NULL
	, [CATEGORY_ID] INT NOT NULL
	, [ITEM_PRICE] NUMERIC(8,2) NOT NULL
);


/* Tabela Order - entidade que reflete as transa��es geradas dentro do site. */
DROP TABLE IF EXISTS [dbo].[FACT_ORDER];
CREATE TABLE [dbo].[FACT_ORDER] (
	[ORDER_ID] INT IDENTITY NOT NULL
	, [ITEM_ID] INT NOT NULL
	, [CUSTOMER_ID] INT NOT NULL
	, [QUANTITY] INT NOT NULL
);

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Cria��o Tabelas Dimens�o
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

-- ITEM_STATE ** Acrescimos em rela��o ao pedido
-- CUSTOMER_SEX ** Acrescimos em rela��o ao pedido

/* Tabela Category - entidade com a descri��o de cada categoria. */
DROP TABLE IF EXISTS [dbo].DIM_CATEGORY;

CREATE TABLE [dbo].DIM_CATEGORY (
	[CATEGORY_ID] INT IDENTITY NOT NULL
	, [CATEGORY_DESCRIPTION] VARCHAR(150) NOT NULL
	, [CATEGORY_PATH] VARCHAR(150) NOT NULL
);

/* Tabela Customer - entidade onde se encontram todos os usu�rios. */
DROP TABLE IF EXISTS [dbo].DIM_CUSTOMER;

CREATE TABLE [dbo].DIM_CUSTOMER (
	[CUSTOMER_ID] INT IDENTITY NOT NULL
	, [CUSTOMER_NAME] VARCHAR(150) NOT NULL
	, [CUSTOMER_SURNAME] VARCHAR(150) NOT NULL
	, [CUSTOMER_GENDER] CHAR NULL
	, [CUSTOMER_TYPE] VARCHAR(15) NOT NULL
	, [CUSTOMER_ADDRESS] VARCHAR(150) NOT NULL
	, [CUSTOMER_BIRTHDAY] DATE NOT NULL
);

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Dados Teste
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Inser��o de Dados fict�cios na tabela de Clientes
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
TRUNCATE TABLE [dbo].DIM_CUSTOMER;

--- Cria��o de Tabela Tempor�ria para gera��o de dados ficticios de clientes
DROP TABLE IF EXISTS #FAKE_CUSTOMER_DATA;
CREATE TABLE #FAKE_CUSTOMER_DATA (
    CUSTOMERNAME VARCHAR(50)
	, CUSTOMERSURNAME VARCHAR(50)
	, CUSTOMERADDRESS VARCHAR(100)
	, CUSTOMERBIRTHDAY DATE
	, CUSTOMERTYPE VARCHAR(15)
);

-- Cria��o de vari�veis para conter lista de nomes poss�veis;
DECLARE @NAMES TABLE (NAMES VARCHAR(50));
DECLARE @SURNAMES TABLE (SURNAMES VARCHAR(50));

INSERT INTO @NAMES (NAMES)
VALUES ('Luc�a'), ('Dolores'), ('Sara'), ('Cristina'), ('Ana'), ('Laura'), ('Isabel'), ('Josefa'), ('Maria'), ('Maria Carmen'), ('Jos� Lu�s'), ('Daniel'), ('Jos� Ant�nio'), ('Javier'), ('Juan'), ('David'), ('Francisco'), ('Jos�'), ('Manuel'), ('Ant�nio');

INSERT INTO @SURNAMES (SURNAMES)
VALUES ('Garc�a'), ('Rodriguez'), ('Gonz�lez'), ('Fernandez'), ('Lopez'), ('Martinez'), ('Sanchez'), ('Perez'), ('Alonso'), ('Gutierrez'), ('Romero'), ('Alvarez'), ('Mu�oz'), ('Moreno'), ('Diaz'), ('Ruiz'), ('Hernandez'), ('Jimenez'), ('Martin'), ('Gomez');

-- Cria��o de vari�veis com o range m�ximo de datas poss�veis para nascimento
DECLARE @STARTDATE DATE = '1970-01-01';
DECLARE @ENDDATE DATE = '2000-12-31';

-- Inserts de dados
INSERT INTO #FAKE_CUSTOMER_DATA (CUSTOMERNAME, CUSTOMERSURNAME, CUSTOMERADDRESS, CUSTOMERBIRTHDAY, CUSTOMERTYPE)
SELECT
    NAMES
	, SURNAMES
	, CUSTOMERADDRESS = 'Address' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR(10))
	, CUSTOMERBIRTHDAY = DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * DATEDIFF(DAY, @STARTDATE, @ENDDATE)), @ENDDATE)
	, CUSTOMERTYPE = CASE
		WHEN ABS(CHECKSUM(NEWID())) % 2 = 0 THEN 'Buyer'
		ELSE 'Seller'
	END
FROM @NAMES
CROSS JOIN @SURNAMES;

INSERT INTO [dbo].DIM_CUSTOMER
SELECT
	CUSTOMERNAME																																		AS CUSTOMER_NAME
	, CUSTOMERSURNAME																																	AS CUSTOMER_SURNAME
	, CASE
		WHEN CUSTOMERNAME IN ('Luc�a', 'Dolores', 'Sara', 'Cristina', 'Ana', 'Laura', 'Isabel', 'Josefa', 'Maria', 'Maria Carmen') THEN 'F'
		WHEN CUSTOMERNAME IN ('Jos� Lu�s', 'Daniel', 'Jos� Ant�nio', 'Javier', 'Juan', 'David', 'Francisco', 'Jos�', 'Manuel', 'Ant�nio') THEN 'M'
		ELSE NULL
	END																																					AS CUSTOMER_GENDER
	, CUSTOMERTYPE																																		AS CUSTOMER_TYPE
	, CUSTOMERADDRESS																																	AS CUSTOMER_ADDRESS
	, CUSTOMERBIRTHDAY																																	AS CUSTOMER_BIRTHDAY
FROM #FAKE_CUSTOMER_DATA;


--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- 
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

TRUNCATE TABLE [dbo].FACT_ITEM;
INSERT INTO [dbo].FACT_ITEM VALUES
	('Samsung Galaxy A21s (SM-A217M/DS) Preto', CAST('2023-05-12' AS DATE), 1, 1079.10)
	, ('Apple iPhone XR 128gb .. De Vitrine Original C/nf E Garantia', CAST('2022-07-07' AS DATE), 1, 2199)
	, ('Xiaomi Pocophone Poco F5 Dual SIM 256 GB preto 8 GB RAM', CAST('2022-06-11' AS DATE), 1, 2846)
	, ('Samsung Galaxy S21 FE 5G (Exynos) 5G Dual SIM 128 GB white 6 GB RAM', NULL, 1, 2581)
	, ('Samsung Galaxy S20 FE 5G 5G Dual SIM 128 GB cloud navy 6 GB RAM', NULL, 1, 1947)
	, ('Moto G5S Plus Dual SIM 32 GB lunar gray 3 GB RAM', CAST('2022-12-11' AS DATE), 1, 599)
	, ('Vitrine Apple iPhone 12 128gb Original - 10x S/ Juros', CAST('2022-11-15' AS DATE), 1, 3699)
	, ('iPhone 11 64gb Preto Original De Vitrine + Nf E Garantia', NULL, 1, 2439)
	, ('Xiaomi Redmi Note 11S Dual SIM 64 GB graphite gray 6 GB RAM', CAST('2021-01-21' AS DATE), 1, 1186)
	, ('Xiaomi 12 Dual SIM 256 GB gray 8 GB RAM', CAST('2022-12-12' AS DATE), 1, 3597)
	

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Inser��o de Dados fict�cios na tabela de Clientes de Ordens
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
TRUNCATE TABLE [dbo].[FACT_ORDER];

DROP TABLE IF EXISTS #FAKE_ORDER_DATA;
CREATE TABLE #FAKE_ORDER_DATA (
    ITEMID INT
	, CUSTOMERID INT
	, QUANTITY INT
);

--- Delimitadores
DECLARE @CUTOMERID_LIMIT INT = 400;
DECLARE @ITEMID_LIMIT INT = 10;
DECLARE @QUANTITY_LIMIT_UP INT = 100;
DECLARE @QUANTITY_LIMIT_DOWN INT = 1;

--- Defini��o da quantidade de registros
WHILE (SELECT COUNT(*) FROM #FAKE_ORDER_DATA) < 1000
BEGIN
    INSERT INTO #FAKE_ORDER_DATA (ITEMID, CUSTOMERID, QUANTITY)
    SELECT 
        ITEMID = ABS(CHECKSUM(NEWID())) % @ITEMID_LIMIT + 1
		, CUSTOMERID = ABS(CHECKSUM(NEWID())) % @CUTOMERID_LIMIT + 1
		, QUANTITY = ABS(CHECKSUM(NEWID())) % (@QUANTITY_LIMIT_UP - @QUANTITY_LIMIT_DOWN + 1) + @QUANTITY_LIMIT_DOWN
		--- Gera a m�trica aleat�riamente definida entre os delimitadores
    FROM (VALUES (1),(2),(3),(4),(5)) AS Numbers(Number)
END


INSERT INTO [dbo].[FACT_ORDER]
SELECT
	ITEMID																																				AS ITEM_ID
	, CUSTOMERID																																		AS CUSTOMER_ID
	, QUANTITY																																			AS QUANTITY
FROM #FAKE_ORDER_DATA;

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Inser��o de Dados na tabela Categoria
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
TRUNCATE TABLE [dbo].DIM_CATEGORY;
INSERT INTO [dbo].DIM_CATEGORY VALUES
	('Celulares e Smartphones', 'Tecnologia > Celulares e Telefones > Celulares e Smartphones')
	, ('Acess�rios para Celulares', 'Tecnologia > Celulares e Telefones > Acess�rios para Celulares')
	, ('Componentes para PC', 'Tecnologia > Inform�tica > Componentes para PC')
	, ('Impress�o', 'Tecnologia > Inform�tica > Impress�o')
	, ('Acess�rios para Notebook', 'Tecnologia > Inform�tica > Acess�rios para Notebook')
	, ('Conectividade e Redes', 'Tecnologia > Inform�tica > Conectividade e Redes')
	, ('Acess�rios para C�meras', 'Tecnologia > C�meras e Acess�rios > Acess�rios para C�meras')
	, ('C�meras', 'Tecnologia > C�meras e Acess�rios > C�meras')
	, ('Acess�rios para �udio e V�deo', 'Tecnologia > Eletr�nicos, �udio e V�deo > Acess�rios para �udio e V�deo')
	, ('�udio Port�til e Acess�rios', 'Tecnologia > Eletr�nicos, �udio e V�deo > �udio Port�til e Acess�rios')
	, ('Componentes Eletr�nicos', 'Tecnologia > Eletr�nicos, �udio e V�deo > Componentes Eletr�nicos')
	, ('Equipamentos para DJs', 'Tecnologia > Eletr�nicos, �udio e V�deo > Equipamentos para DJs')
	, ('Video Games', 'Tecnologia > Games > Video Games')
	, ('Fliperama e Arcade', 'Tecnologia > Games > Fliperama e Arcade')
	, ('Televisores', 'Tecnologia > Televisores')