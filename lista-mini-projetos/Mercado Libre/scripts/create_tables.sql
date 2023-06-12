--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- SCRIPTS DDL
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Criação do Banco de Dados Utilizado
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
-- Script base para utilização do Banco de Dados definido
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
/* Sempre que utilizarmos o prefixo com o nome do Banco de Dados de agora em diante, executaremos uma string SQL. Deste modo, caso seja necessário criar um Banco de Dados teste, basta somente alterar a variável @dbname */

DECLARE @SQL NVARCHAR(128)
SET @sql = N'USE ' + QUOTENAME(@dbname)

EXEC sp_executesql @sql
GO


-- criar tabela temporária como ## para não precisar declarar duas vezes a variavel

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Criação Tabelas Fato
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


/* Tabela Order - entidade que reflete as transações geradas dentro do site. */
DROP TABLE IF EXISTS [dbo].[FACT_ORDER];
CREATE TABLE [dbo].[FACT_ORDER] (
	[ORDER_ID] INT IDENTITY NOT NULL
	, [ITEM_ID] INT NOT NULL
	, [CUSTOMER_ID] INT NOT NULL
	, [QUANTITY] INT NOT NULL
);

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Criação Tabelas Dimensão
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

-- ITEM_STATE ** Acrescimos em relação ao pedido
-- CUSTOMER_SEX ** Acrescimos em relação ao pedido

/* Tabela Category - entidade com a descrição de cada categoria. */
DROP TABLE IF EXISTS [dbo].DIM_CATEGORY;

CREATE TABLE [dbo].DIM_CATEGORY (
	[CATEGORY_ID] INT IDENTITY NOT NULL
	, [CATEGORY_DESCRIPTION] VARCHAR(150) NOT NULL
	, [CATEGORY_PATH] VARCHAR(150) NOT NULL
);

/* Tabela Customer - entidade onde se encontram todos os usuários. */
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

/* Inserção de Dados fictícios na tabela de Clientes */
TRUNCATE TABLE [dbo].DIM_CUSTOMER;

--- Criação de Tabela Temporária para geração de dados ficticios de clientes
DROP TABLE IF EXISTS #FAKE_CUSTOMER_DATA;
CREATE TABLE #FAKE_CUSTOMER_DATA (
    CUSTOMERID INT
	, CUSTOMERNAME VARCHAR(50)
	, CUSTOMERSURNAME VARCHAR(50)
	, CUSTOMERADDRESS VARCHAR(100)
	, CUSTOMER_BIRTHDAY DATE
	, CUSTOMERTYPE VARCHAR(15)
);

-- Criação de variáveis para conter lista de nomes possíveis;
DECLARE @NAMES TABLE (NAMES VARCHAR(50));
DECLARE @SURNAMES TABLE (SURNAMES VARCHAR(50));

INSERT INTO @NAMES (NAMES)
VALUES ('Lucía'), ('Dolores'), ('Sara'), ('Cristina'), ('Ana'), ('Laura'), ('Isabel'), ('Josefa'), ('Maria'), ('Maria Carmen'), ('José Luís'), ('Daniel'), ('José António'), ('Javier'), ('Juan'), ('David'), ('Francisco'), ('José'), ('Manuel'), ('António');

INSERT INTO @SURNAMES (SURNAMES)
VALUES ('García'), ('Rodriguez'), ('González'), ('Fernandez'), ('Lopez'), ('Martinez'), ('Sanchez'), ('Perez'), ('Alonso'), ('Gutierrez'), ('Romero'), ('Alvarez'), ('Muñoz'), ('Moreno'), ('Diaz'), ('Ruiz'), ('Hernandez'), ('Jimenez'), ('Martin'), ('Gomez');

-- Criação de variáveis com o range máximo de datas possíveis para nascimento
DECLARE @STARTDATE DATE = '1970-01-01';
DECLARE @ENDDATE DATE = '2000-12-31';


INSERT INTO #FAKE_CUSTOMER_DATA (CUSTOMERID, CUSTOMERNAME, CUSTOMERSURNAME, CUSTOMERADDRESS, CUSTOMER_BIRTHDAY, CUSTOMERTYPE)
SELECT
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS CUSTOMERID
	, NAMES
	, SURNAMES
	, 'Address' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR(10)) AS CUSTOMERADDRESS
	, DATEADD(DAY, -FLOOR(RAND(CHECKSUM(NEWID())) * DATEDIFF(DAY, @STARTDATE, @ENDDATE)), @ENDDATE)  AS Birthday
	, CASE
		WHEN ABS(CHECKSUM(NEWID())) % 2 = 0 THEN 'Buyer'
		ELSE 'Seller'
	END AS CUSTOMERTYPE
FROM @NAMES
CROSS JOIN @SURNAMES;

INSERT INTO [dbo].DIM_CUSTOMER
SELECT
	CUSTOMERNAME
	, CUSTOMERSURNAME
	, CASE
		WHEN CUSTOMERNAME IN ('Lucía', 'Dolores', 'Sara', 'Cristina', 'Ana', 'Laura', 'Isabel', 'Josefa', 'Maria', 'Maria Carmen') THEN 'F'
		WHEN CUSTOMERNAME IN ('José Luís', 'Daniel', 'José António', 'Javier', 'Juan', 'David', 'Francisco', 'José', 'Manuel', 'António') THEN 'M'
		ELSE NULL
	END AS CUSTOMER_GENDER
	, CUSTOMERTYPE
	, CUSTOMERADDRESS
	, CUSTOMER_BIRTHDAY
FROM #FAKE_CUSTOMER_DATA;


/*  */
TRUNCATE TABLE [dbo].FACT_ITEM;
INSERT INTO [dbo].FACT_ITEM VALUES
	('Samsung Galaxy A21s (SM-A217M/DS) Preto', '12/05/2023', 1, 1079.10)


/*  */
TRUNCATE TABLE [dbo].[FACT_ORDER];
INSERT INTO [dbo].[FACT_ORDER] VALUES
	(3, 1, 1)


/* Inserção de Dados na tabela Categoria */
TRUNCATE TABLE [dbo].DIM_CATEGORY;
INSERT INTO [dbo].DIM_CATEGORY VALUES
	('Celulares e Smartphones', 'Tecnologia > Celulares e Telefones > Celulares e Smartphones')
	, ('Acessórios para Celulares', 'Tecnologia > Celulares e Telefones > Acessórios para Celulares')
	, ('Componentes para PC', 'Tecnologia > Informática > Componentes para PC')
	, ('Impressão', 'Tecnologia > Informática > Impressão')
	, ('Acessórios para Notebook', 'Tecnologia > Informática > Acessórios para Notebook')
	, ('Conectividade e Redes', 'Tecnologia > Informática > Conectividade e Redes')
	, ('Acessórios para Câmeras', 'Tecnologia > Câmeras e Acessórios > Acessórios para Câmeras')
	, ('Câmeras', 'Tecnologia > Câmeras e Acessórios > Câmeras')
	, ('Acessórios para Áudio e Vídeo', 'Tecnologia > Eletrônicos, Áudio e Vídeo > Acessórios para Áudio e Vídeo')
	, ('Áudio Portátil e Acessórios', 'Tecnologia > Eletrônicos, Áudio e Vídeo > Áudio Portátil e Acessórios')
	, ('Componentes Eletrônicos', 'Tecnologia > Eletrônicos, Áudio e Vídeo > Componentes Eletrônicos')
	, ('Equipamentos para DJs', 'Tecnologia > Eletrônicos, Áudio e Vídeo > Equipamentos para DJs')
	, ('Video Games', 'Tecnologia > Games > Video Games')
	, ('Fliperama e Arcade', 'Tecnologia > Games > Fliperama e Arcade')
	, ('Televisores', 'Tecnologia > Televisores')