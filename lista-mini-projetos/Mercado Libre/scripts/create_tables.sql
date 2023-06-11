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

/* Inser��o de Dados fict�cios na tabela de Clientes */
TRUNCATE TABLE [dbo].DIM_CUSTOMER;

DROP TABLE IF EXISTS #FakeCustomers;
CREATE TABLE #FakeCustomers (
    CustomerID INT
	, FirstName VARCHAR(50)
	, LastName VARCHAR(50)
	, Email VARCHAR(100)
	, Address VARCHAR(100)
);

DECLARE @FirstNames TABLE (FirstName VARCHAR(50));
DECLARE @Surnames TABLE (Surname VARCHAR(50));

INSERT INTO @FirstNames (FirstName)
VALUES ('Luc�a'), ('Dolores'), ('Sara'), ('Cristina'), ('Ana'), ('Laura'), ('Isabel'), ('Josefa'), ('Maria'), ('Maria Carmen'), ('Jos� Lu�s'), ('Daniel'), ('Jos� Ant�nio'), ('Javier'), ('Juan'), ('David'), ('Francisco'), ('Jos�'), ('Manuel'), ('Ant�nio');

INSERT INTO @Surnames (Surname)
VALUES ('Garc�a'), ('Rodriguez'), ('Gonz�lez'), ('Fernandez'), ('Lopez'), ('Martinez'), ('Sanchez'), ('Perez'), ('Alonso'), ('Gutierrez'), ('Romero'), ('Alvarez'), ('Mu�oz'), ('Moreno'), ('Diaz'), ('Ruiz'), ('Hernandez'), ('Jimenez'), ('Martin'), ('Gomez');


INSERT INTO #FakeCustomers (CustomerID, FirstName, LastName, Email, Customer_Address)
SELECT
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS CustomerID
	, FirstName
	, Surname
	, 'email' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR(10)) + '@example.com' AS Email
	, 'Address' + CAST(ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS VARCHAR(10)) AS Customer_Address
FROM @FirstNames
CROSS JOIN @Surnames;


INSERT INTO [dbo].DIM_CUSTOMER VALUES
	('Lucas', 'Castro', 'M', 'Buyer', 'Av. Sumar�', '03/07/1994')
SELECT
	FirstName
	, LastName
	, CASE
		WHEN FirstName IN ('Luc�a', 'Dolores', 'Sara', 'Cristina', 'Ana', 'Laura', 'Isabel', 'Josefa', 'Maria', 'Maria Carmen') THEN 'F'
		WHEN FirstName IN ('Jos� Lu�s', 'Daniel', 'Jos� Ant�nio', 'Javier', 'Juan', 'David', 'Francisco', 'Jos�', 'Manuel', 'Ant�nio') THEN 'M'
		ELSE NULL
	END AS Gender
	, 
	, Customer_Address
	, 
FROM #FakeCustomers;


/*  */
TRUNCATE TABLE [dbo].FACT_ITEM;
INSERT INTO [dbo].FACT_ITEM VALUES
	('Samsung Galaxy A21s (SM-A217M/DS) Preto', '12/05/2023', 1, 1079.10)


/*  */
TRUNCATE TABLE [dbo].[FACT_ORDER];
INSERT INTO [dbo].[FACT_ORDER] VALUES
	(3, 1, 1)


/*  */
TRUNCATE TABLE [dbo].DIM_CATEGORY;
INSERT INTO [dbo].DIM_CATEGORY VALUES
	('Telefones e smartphones', '')