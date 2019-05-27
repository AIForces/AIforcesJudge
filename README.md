# AIforces Judge

This project is a part of [AIforces](https://github.com/aalekseevx/AIforces)

AIforces Judge is a separated multithreaded judging system for game bots competitions.
Works only on Unux. (Tested only on Ubuntu)
## Get started
The system is written in python3 and uses firejail as a sandbox

#### Prerequisites
* `python3`
* `pipenv`
* `venv`
* `firejail`

Installation on ubuntu-based systems.
Satisfy the prerequisites

```bash
sudo apt-get install pipenv python3-venv firejail
```

After that, clone repository and install python packages

```bash
git clone https://github.com/AbsoluteNikola/AIforcesJudge.git
cd AIforcesJudge
pipenv update
```

Finally, start the application.
```bash
pipenv run s
```

#### Advanced
if you want to setup system as systemd unit run this commands
```bash
sudo ln -s FULL_PATH_TO_AIforcesJudge/config/ai_forces_judge.service /etc/systemd/system
# don't forgot to change working dir in config
sudo systemctl daemon-reload
sudo systemctl enable ai_forces_judge.service
sudo systemctl start ai_forces_judge.service
```

## Authors

* **Aleksandr Alekseev ([aalekseevx](https://github.com/aalekseevx))** - Rails and Web Design 
* **Nikolay Rulev ([AbsoluteNikola](https://github.com/AbsoluteNikola))** - Multithreaded judging system

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
