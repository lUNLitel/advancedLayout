from animatic_builder.model import Project


def test_auto_shot_naming_increments_by_ten():
    project = Project()
    s1 = project.add_shot("a.mp4")
    s2 = project.add_shot("b.mp4")
    assert s1.name == "shot_010"
    assert s2.name == "shot_020"


def test_replace_preserves_name_and_comment_and_clamps_trim(tmp_path):
    project = Project()
    shot = project.add_shot("a.mp4", trim_in=1.0, trim_out=9.0)
    shot.comment = "hello"
    project.replace_media(0, "b.mp4", media_length=5.0)

    replaced = project.shots[0]
    assert replaced.file_path == "b.mp4"
    assert replaced.name == "shot_010"
    assert replaced.comment == "hello"
    assert replaced.trim_out == 5.0


def test_save_load_round_trip(tmp_path):
    project = Project()
    shot = project.add_shot("clip.mp4")
    shot.comment = "note"

    path = tmp_path / "project.animatic.json"
    project.save(path)
    loaded = Project.load(path)

    assert len(loaded.shots) == 1
    assert loaded.shots[0].name == "shot_010"
    assert loaded.shots[0].comment == "note"
