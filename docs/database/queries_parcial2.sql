-- a) Tickets abiertos con el nombre del solicitante mediante JOIN
SELECT 
    t.id AS ticket_id,
    t.title AS titulo_ticket,
    u.full_name AS nombre_solicitante,
    t.status AS estado
FROM tickets t
JOIN users u ON t.requester_id = u.id
WHERE t.status = 'OPEN';

-- b) Conteo de tickets por técnico asignado
SELECT 
    u.id AS tecnico_id,
    u.full_name AS nombre_tecnico,
    COUNT(t.id) AS total_tickets
FROM users u
JOIN tickets t ON u.id = t.assigned_tech_id
GROUP BY u.id, u.full_name
HAVING COUNT(t.id) > 0
ORDER BY total_tickets DESC;

-- c) Tickets sin comentarios mediante LEFT JOIN
SELECT 
    t.id AS ticket_id,
    t.title AS titulo_ticket
FROM tickets t
LEFT JOIN ticket_comments c ON t.id = c.ticket_id
WHERE c.id IS NULL;

-- d) Demostración de ON DELETE CASCADE dentro de BEGIN y ROLLBACK
BEGIN;

SELECT COUNT(*) AS conteo_inicial_historial 
FROM ticket_history 
WHERE ticket_id = 1;

DELETE FROM tickets WHERE id = 1;

SELECT COUNT(*) AS conteo_tras_delete 
FROM ticket_history 
WHERE ticket_id = 1;

ROLLBACK;

SELECT COUNT(*) AS conteo_tras_rollback 
FROM ticket_history 
WHERE ticket_id = 1;