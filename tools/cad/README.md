# CAD sheet engine

Generates construction-document sheets as a 24" x 36" (ARCH D) plot PDF and an AutoCAD-compatible DXF (R12, model space in inches, AIA layer names).

```
python3 a101_1.py ../../drawings/construction-documents
```

- `cadkit.py`: sheet, layers, line weights, PDF and DXF writers
- `plan_engine.py`: rooms to walls by type (W1, W2, E1, P1), wall poché, doors, windows, dimensions and tags
- `a101_1.py`: sheet A-101.1, Model 1 ground floor plan
