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
	PRINT 'db exists. Please choose another name.'
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

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Criação Tabelas Fato
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
/* Tabela Customer - entidade onde se encontram todos os usuários. */
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

/* Tabela Order - entidade que reflete as transações geradas dentro do site. */
CREATE TABLE [dbo].[FACT_ORDER] (
	[ORDER_ID] INT IDENTITY NOT NULL
	, [ITEM_ID] INT NOT NULL
	, [CUSTOMER_ID] INT NOT NULL
);


--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Criação Tabelas Dimensão
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=

-- ITEM_STATE ** Acrescimos em relação ao pedido
-- CUSTOMER_SEX ** Acrescimos em relação ao pedido

/* Tabela Category - entidade com a descrição de cada categoria. */
CREATE TABLE [dbo].DIM_CATEGORY (
	[CATEGORY_ID] INT IDENTITY NOT NULL
	, [CATEGORY_DESCRIPTION] VARCHAR(150) NOT NULL
	, [CATEGORY_PATH] VARCHAR(150) NOT NULL
);

--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=
-- Dados Teste
--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=--=