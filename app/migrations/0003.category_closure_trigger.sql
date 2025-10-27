CREATE OR REPLACE FUNCTION category_closure_insert()
RETURNS TRIGGER AS $$
BEGIN

  INSERT INTO category_closure (ancestor, descendant, depth)
  VALUES (NEW.id, NEW.id, 0);

  IF NEW.parent_id IS NOT NULL THEN
    INSERT INTO category_closure (ancestor, descendant, depth)
    SELECT ancestor, NEW.id, depth + 1
    FROM category_closure
    WHERE descendant = NEW.parent_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_category_closure_insert
AFTER INSERT ON categories
FOR EACH ROW EXECUTE FUNCTION category_closure_insert();