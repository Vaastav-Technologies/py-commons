# Contributing to vt-commons

Thank you for your interest in contributing to the project! We welcome all kinds of contributions: bug reports, feature requests, documentation improvements, or code enhancements.

---

## 🧑‍💻 Development Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/Vaastav-Technologies/py-commons.git
    cd py-commons
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**

Using pip:

    ```bash
    pip install -e . --group dev
    ```

Using [uv](https://github.com/astral-sh/uv) (automatically includes dev dependencies):

    ```bash
    uv pip install -e .
    ```

This installs both the project and the developer dependencies.

---

## 🧪 Running Tests

We use `pytest` for testing.

    ```bash
    pytest --doctest-modules
    ```

---

## 🧼 Code Style & Linting

We follow PEP8. Use `ruff` for all linting and formatting tasks.

* Check for lint errors:

    ```bash
    ruff check
    ```

* Check formatting (CI-safe):

    ```bash
    ruff format --check
    ```

* Auto-format code:

    ```bash
    ruff format
    ```

---

## 🧠 Tips for Contributors

* Write docstrings for all public classes and functions.
* Add usage examples (doctests for all public facing API and where applicable in private APIs).
* Treat doctests as first class testing and use pytest/mock when complex testing is required.
* Update the README with any user-facing changes.
* Write or update tests for new features or bugfixes.

---

## 🔃 Submitting Changes

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them with clear messages.

    Commit message format:

    ```text
    <feature-affector-or-id-to-track>: <A message summary subject>
    
    <The detailed message description>
    ```

4. Push to your fork: `git push origin feature-name`
5. Open a Pull Request and describe your changes.

---

## 📞 Need Help?

Open an issue or contact a maintainer. We're happy to help!
