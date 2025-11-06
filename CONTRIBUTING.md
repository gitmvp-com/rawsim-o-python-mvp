# Contributing to RAWSim-O Python MVP

Thank you for your interest in contributing! This project is an MVP implementation and welcomes contributions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/rawsim-o-python-mvp.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Add docstrings to classes and functions
- Keep functions focused and concise

### Project Structure

- `core/` - Core simulation elements (bots, pods, waypoints, etc.)
- `pathfinding/` - Pathfinding algorithms
- `control/` - Control systems and strategies
- `simulation/` - Simulation execution engine
- `statistics/` - Statistics tracking and export
- `visualization/` - 2D visualization with Pygame
- `utils/` - Utility functions
- `generator/` - Instance generation

### Adding New Features

1. **New Pathfinding Algorithm**
   - Add to `pathfinding/` directory
   - Implement interface compatible with existing algorithms
   - Update `PathPlanner` to support new method

2. **New Control Strategy**
   - Add to `control/` directory
   - Follow existing patterns (TaskManager, PodSelector)
   - Document algorithm and parameters

3. **New Visualization**
   - Consider web-based (Three.js) or 3D (Panda3D)
   - Maintain compatibility with existing simulation

### Testing

Before submitting:

1. Test your changes locally
2. Run CLI mode: `python cli.py --generate`
3. Run visual mode: `python visualization.py --generate`
4. Verify no errors in logs

## Areas for Contribution

### High Priority

- [ ] Additional pathfinding algorithms (CBS, PAS, BCP)
- [ ] Order generation system
- [ ] Item picking/storing logic
- [ ] Performance optimizations
- [ ] Unit tests

### Medium Priority

- [ ] 3D visualization (web-based or Panda3D)
- [ ] Configuration validation
- [ ] More statistical metrics
- [ ] Multi-threaded simulation
- [ ] Real-time monitoring dashboard

### Nice to Have

- [ ] Machine learning integration
- [ ] Benchmark suite
- [ ] Docker containerization
- [ ] Documentation website
- [ ] Tutorial notebooks

## Pull Request Process

1. Update README.md if you've added features
2. Update docstrings and comments
3. Ensure code follows style guidelines
4. Test thoroughly
5. Submit PR with clear description

## Questions?

Open an issue or discussion on GitHub.

## License

By contributing, you agree that your contributions will be licensed under GPL-3.0.
