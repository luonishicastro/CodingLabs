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
	PRINT 'db exists. Please choose another name.'
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

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Cria��o Tabelas Fato
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
/* Tabela Customer - entidade onde se encontram todos os usu�rios. */
DROP TABLE IF EXISTS [dbo].FACT_CUSTOMER;

CREATE TABLE [dbo].FACT_CUSTOMER (
	[CUSTOMER_ID] INT IDENTITY NOT NULL
	, [CUSTOMER_NAME] VARCHAR(150) NOT NULL
	, [CUSTOMER_SURNAME] VARCHAR(150) NOT NULL
	, [CUSTOMER_SEX] CHAR NOT NULL
	, [CUSTOMER_ADDRESS] VARCHAR(150) NOT NULL
	, [CUSTOMER_BIRTHDAY] DATE NOT NULL
);

/* Tabela Item - entidade onde se encontram os produtos publicados no marketplace. */
CREATE TABLE [dbo].FACT_ITEM (
	[ITEM_ID] INT IDENTITY NOT NULL
	, [PRODUCT_NAME] VARCHAR(150) NOT NULL
	, [ITEM_STATE] AS IIF(ISNULL([END_DATE], '') = '', 'A', 'I')
	, [END_DATE] DATETIME NULL
	, [CATEGORY_ID] INT NOT NULL
);

/* Tabela Order - entidade que reflete as transa��es geradas dentro do site. */
CREATE TABLE [dbo].[FACT_ORDER] (
	[ORDER_ID] INT IDENTITY NOT NULL
	, [ITEM_ID] INT NOT NULL
	, [CUSTOMER_ID] INT NOT NULL
);


--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Cria��o Tabelas Dimens�o
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

-- ITEM_STATE ** Acrescimos em rela��o ao pedido
-- CUSTOMER_SEX ** Acrescimos em rela��o ao pedido

/* Tabela Category - entidade com a descri��o de cada categoria. */
CREATE TABLE [dbo].DIM_CATEGORY (
	[CATEGORY_ID] INT IDENTITY NOT NULL
	, [CATEGORY_DESCRIPTION] VARCHAR(150) NOT NULL
	, [CATEGORY_PATH] VARCHAR(150) NOT NULL
);

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Dados Teste
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=