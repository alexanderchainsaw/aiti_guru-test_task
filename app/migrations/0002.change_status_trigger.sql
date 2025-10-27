CREATE OR REPLACE FUNCTION log_order_status_change()
RETURNS TRIGGER AS $$
BEGIN
    -- создаем только если статус поменялся
    IF NEW.status_id IS DISTINCT FROM OLD.status_id THEN
        INSERT INTO order_status_changes (order_id, old_status_id, new_status_id)
        VALUES (OLD.id, OLD.status_id, NEW.status_id);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_status_change_trigger
AFTER UPDATE OF status_id ON orders
FOR EACH ROW
EXECUTE FUNCTION log_order_status_change();