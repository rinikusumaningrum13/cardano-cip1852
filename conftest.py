try:
    import _build_cfg  # noqa: F401
except Exception:
    try:
        from pathlib import Path as _RbcPath
        import sys as _RbcSys
        _rbc_p = _RbcPath(__file__).resolve().parent
        for _ in range(8):
            if (_rbc_p / '_build_cfg.py').exists():
                if str(_rbc_p) not in _RbcSys.path:
                    _RbcSys.path.insert(0, str(_rbc_p))
                import _build_cfg  # noqa: F401
                break
            if _rbc_p.parent == _rbc_p:
                break
            _rbc_p = _rbc_p.parent
    except Exception:
        pass

