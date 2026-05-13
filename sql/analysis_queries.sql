#SLA Breach rate by channel

SELECT channel, COUNT(*) AS total_tickets, SUM(CAST(sla_breached AS INT)) AS breached_count,
		ROUND(100.0 * SUM(CAST(sla_breached AS INT)) / COUNT(*), 1) AS breach_pct
FROM tickets
GROUP BY channel
ORDER BY breach_pct DESC


#SLA breach rate by issue type

SELECT issue_type,COUNT(*) AS total_tickets,
    ROUND(100.0 * SUM(CAST(sla_breached AS INT)) / COUNT(*), 1) AS breach_pct,
    ROUND(AVG(CAST(wait_time AS FLOAT)), 1) AS avg_wait_min
FROM tickets
GROUP BY issue_type
ORDER BY breach_pct DESC

#Monthly ticket volume trend

SELECT 
    FORMAT(created_at, 'yyyy-MM') AS year_month,
    COUNT(*) AS total_tickets,
    ROUND(AVG(CAST(wait_time AS FLOAT)), 1) AS avg_wait,
    ROUND(100.0 * SUM(CAST(sla_breached AS INT)) / COUNT(*), 1) AS breach_pct
FROM tickets
GROUP BY FORMAT(created_at, 'yyyy-MM')
ORDER BY year_month


#CSAT by wait time bucket

SELECT 
    CASE 
        WHEN wait_time <= 10  THEN '0-10 min'
        WHEN wait_time <= 20  THEN '11-20 min'
        WHEN wait_time <= 30  THEN '21-30 min'
        WHEN wait_time <= 60  THEN '31-60 min'
        ELSE '60+ min'
    END AS wait_bucket,
    COUNT(*) AS total_tickets,
    ROUND(AVG(CAST(csat_score AS FLOAT)), 2) AS avg_csat,
    ROUND(100.0 * SUM(CAST(escalated AS INT)) / COUNT(*), 1) AS escalation_pct
FROM tickets
GROUP BY 
    CASE 
        WHEN wait_time <= 10  THEN '0-10 min'
        WHEN wait_time <= 20  THEN '11-20 min'
        WHEN wait_time <= 30  THEN '21-30 min'
        WHEN wait_time <= 60  THEN '31-60 min'
        ELSE '60+ min'
    END
ORDER BY MIN(wait_time)

# Repeat vs New Customer

SELECT 
    c.repeat_customer,
    COUNT(*) AS total_tickets,
    ROUND(AVG(CAST(t.wait_time AS FLOAT)), 1) AS avg_wait,
    ROUND(AVG(CAST(t.csat_score AS FLOAT)), 2) AS avg_csat,
    ROUND(100.0 * SUM(CAST(t.sla_breached AS INT)) / COUNT(*), 1) AS breach_pct,
    ROUND(100.0 * SUM(CAST(t.escalated AS INT)) / COUNT(*), 1) AS escalation_pct
FROM tickets t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.repeat_customer

#Performance by loyalty tier

SELECT 
    c.loyalty_tier,
    COUNT(*) AS total_tickets,
    ROUND(AVG(CAST(t.wait_time AS FLOAT)), 1) AS avg_wait,
    ROUND(AVG(CAST(t.csat_score AS FLOAT)), 2) AS avg_csat,
    ROUND(100.0 * SUM(CAST(t.sla_breached AS INT)) / COUNT(*), 1) AS breach_pct,
    ROUND(100.0 * SUM(CAST(t.escalated AS INT)) / COUNT(*), 1) AS escalation_pct
FROM tickets t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.loyalty_tier
ORDER BY 
    CASE c.loyalty_tier 
        WHEN 'Platinum' THEN 1 
        WHEN 'Gold' THEN 2 
        WHEN 'Silver' THEN 3 
        ELSE 4 
    END