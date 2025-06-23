import streamlit as st
import graphviz

st.set_page_config(page_title="Python Memory Visualizer", layout="centered")
st.title("Python Memory Reference Visualizer")

st.markdown("""
This tool simulates how Python variables point to memory objects. 
Try entering simple assignments like:
```python
x = 10
y = x
y += 1
```
OR for mutable types:
```python
a = [1, 2, 3]
b = a
b.append(4)
```
""")

user_code = st.text_area(
    "✍️ Enter your Python code:",
    height=200,
    value="""x = 10
y = x
y += 1"""
)

if st.button("🚀 Visualize"):
    try:
        local_vars = {}
        exec(user_code, {}, local_vars)

        object_ids = {}
        references = {}

        for var, value in local_vars.items():
            obj_id = id(value)
            if obj_id not in object_ids:
                object_ids[obj_id] = value
            references[var] = obj_id

        dot = graphviz.Digraph()

        # Fixed Memory Cluster (forced layout look using rank and fixed padding)
        with dot.subgraph(name='cluster_memory') as mem:
            mem.attr(label='Memory', style='filled', color='lightgrey', margin="1.0", labelloc="t")
            mem.attr(rank="same")  # keep them on the same horizontal level

            # Add padding nodes to simulate a fixed large box visually
            for i in range(3):
                mem.node(f"pad_left_{i}", label="", width="0.01", style="invis")
                mem.node(f"pad_right_{i}", label="", width="0.01", style="invis")

            for obj_id, val in object_ids.items():
                label = f"{val}\n(id: {obj_id})"
                mem.node(str(obj_id), label=label, shape="box", style="filled", color="#E6F2FF", width="2", height="1.5")

        # Variables outside memory
        for var, obj_id in references.items():
            dot.node(var, shape="ellipse", style="filled", color="#FFEDD5", width="1.5", height="1.5")
            dot.edge(var, str(obj_id))

        st.graphviz_chart(dot)

        st.success("Visualization complete! ✅")
    except Exception as e:
        st.error(f"❌ Error: {e}")
