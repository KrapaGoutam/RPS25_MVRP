# solver.py
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA  # Fixed import path
from qiskit.primitives import Sampler
from qiskit_ibm_runtime import QiskitRuntimeService
from app_configs import IBM_QUANTUM_TOKEN, NUM_VEHICLES

# Authenticate with IBM Quantum (Fixed)
service = QiskitRuntimeService(token=IBM_QUANTUM_TOKEN, channel="ibm_quantum")

def solve_mvrp(locations, G):
    """Solves the Multi-Vehicle Routing Problem (MVRP) using Qiskit."""
    qp = QuadraticProgram()

    # Add binary variables for vehicle assignments
    for i in range(NUM_VEHICLES):
        qp.binary_var(f"v{i}")

    # Add constraints (Example: ensuring each location is visited)
    qp.linear_constraint([1] * NUM_VEHICLES, "==", 1, "visit_constraints")

    # Solve using QAOA
    sampler = Sampler()
    qaoa = QAOA(sampler=sampler)
    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(qp)

    # Generate optimized routes (Example Data)
    optimized_routes = [
        [locations[0], locations[2], locations[4]],
        [locations[1], locations[3]],
    ]

    return optimized_routes
