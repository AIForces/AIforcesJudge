# AIforces Judge

This project is a part of [AIforces](https://github.com/aalekseevx/AIforces)

AIforces Judge is separated multithreaded judging system for game bots competitions.
Works only on Linux.
## Get started
the system is written in python3 and uses firejail as sandbox

####Prerequisites
* `python3`
* `pipenv`
* `venv`
* `firejail`

If use ubuntu based systems you can run 

```bash
sudo apt-get install pipenv python3-venv firejail
```

After it you can clone repository and install python packages

```bash
git clone https://github.com/AbsoluteNikola/AIforcesJudge.git
cd AIforcesJudge
pipenv update
```

and last step to do is just run this command
```bash
pipenv run s
```

####Advanced
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
