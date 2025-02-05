# solver.py
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit.primitives import Sampler
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_algorithms.optimizers import COBYLA  # ✅ Added optimizer import
import networkx as nx
from app_configs import IBM_QUANTUM_TOKEN

# Authenticate with IBM Quantum
service = QiskitRuntimeService(token=IBM_QUANTUM_TOKEN, channel="ibm_quantum")

def solve_mvrp(locations, G, num_vehicles):
    """Solves the Multi-Vehicle Routing Problem (MVRP) using Qiskit.

    Args:
        locations (list): List of client locations.
        G (networkx.Graph): The graph/network of routes.
        num_vehicles (int): The number of vehicles.

    Returns:
        list: A list of optimized routes per vehicle.
    """
    if num_vehicles > 5:
        print("⚠ Warning: Reducing num_vehicles to avoid excessive memory usage")
        num_vehicles = 5  # ✅ Limit max vehicles to 5 to avoid large memory usage

    if len(locations) > 20:
        print("⚠ Warning: Reducing num_clients to avoid excessive problem size")
        locations = locations[:20]  # ✅ Limit clients to 20 to prevent exponential scaling

    qp = QuadraticProgram()

    # Create binary variables for vehicle assignments
    vehicle_vars = {}
    for v in range(num_vehicles):
        for i in range(len(locations)):
            var_name = f"v{v}_loc{i}"
            vehicle_vars[(v, i)] = qp.binary_var(var_name)

    # Constraint: Each location must be visited exactly once
    for i in range(len(locations)):
        qp.linear_constraint(
            linear={f"v{v}_loc{i}": 1 for v in range(num_vehicles)},  
            sense="==",
            rhs=1,
            name=f"visit_loc_{i}"
        )

    # Objective function: Minimize total travel cost
    obj_expr = {}
    for v in range(num_vehicles):
        for i in range(len(locations)):
            for j in range(len(locations)):
                if i != j and locations[i] in G and locations[j] in G[locations[i]]:
                    cost = G[locations[i]][locations[j]]["weight"]
                    var_name = f"v{v}_loc{i}"
                    obj_expr[var_name] = obj_expr.get(var_name, 0) + cost  

    qp.minimize(linear=obj_expr)

    # ✅ Fix: Provide an optimizer for QAOA
    sampler = Sampler()
    optimizer = COBYLA(maxiter=100)  # ✅ Reduce iterations to avoid long computations
    qaoa = QAOA(sampler=sampler, optimizer=optimizer)  # ✅ Now includes optimizer

    optimizer_qiskit = MinimumEigenOptimizer(qaoa)

    try:
        result = optimizer_qiskit.solve(qp)
    except MemoryError as e:
        print(f"❌ MemoryError: {e}")
        return [[] for _ in range(num_vehicles)]  # ✅ Return an empty result on failure

    # Extract optimized vehicle assignments
    optimized_routes = [[] for _ in range(num_vehicles)]
    solution = result.samples[0].x  

    for (v, i) in vehicle_vars:
        var_name = f"v{v}_loc{i}"
        if solution[qp.get_variable_index(var_name)] == 1:  
            optimized_routes[v].append(locations[i])

    return optimized_routes
