DECLARE @dbname nvarchar(128)
SET @dbname = N'BD_MERCADOLIBRE'

PRINT 'Please keep it the same name as defined on create_tables.sql'

DECLARE @SQL NVARCHAR(128)
SET @sql = N'USE ' + QUOTENAME(@dbname)

EXEC sp_executesql @sql
GO

/* Listar os usuários que fazem aniversário no dia de hoje e que a quantidade de vendas realizadas em Janeiro/2020 sejam superiores a 1500; */

CREATE OR ALTER VIEW VIEW_EXERCICIO_1
AS
	SELECT
		ORD.CUSTOMER_ID
		, YEAR([END_DATE])*100+MONTH([END_DATE])								AS YEAR_MONTH
		, SUM(ITM.ITEM_PRICE)											AS TOTAL
	FROM [dbo].[FACT_ORDER] ORD
	LEFT JOIN [dbo].FACT_ITEM ITM
		ON ITM.ITEM_ID = ORD.ITEM_ID
	LEFT JOIN [dbo].DIM_CUSTOMER CST
		ON CST.CUSTOMER_ID = ORD.CUSTOMER_ID
	WHERE YEAR([END_DATE])*100+MONTH([END_DATE])=202001 --
		AND CAST(CST.CUSTOMER_BIRTHDAY AS DATE) = CAST(GETDATE() AS DATE) --
	GROUP BY
		ORD.CUSTOMER_ID
		, YEAR([END_DATE])*100+MONTH([END_DATE])
	HAVING SUM(ITM.ITEM_PRICE) > 1500
GO

/* Para cada mês de 2020, solicitamos que seja exibido um top 5 dos usuários que mais venderam ($) na categoria Celulares. Solicitamos o mês e ano da análise, nome e sobrenome do vendedor, quantidade de vendas realizadas, quantidade de produtos vendidos e o total vendido; */

CREATE OR ALTER VIEW VIEW_EXERCICIO_2
AS