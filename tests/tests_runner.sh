if [[ $1 == "s" ]]; then
    # run sovler tests
    pytest -v test_01_solver.py
elif [[ $1 == "g" ]]; then 
    # run generator tests
    pytest -v test_02_generator.py
else
    # run both tests
    pytest -v 
fi
