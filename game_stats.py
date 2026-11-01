from pathlib import Path

class GameStats: 
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self._read_high_score()
    
    def _read_high_score(self):
        path = Path('high_score.txt')

        if path.exists():
            contents = path.read_text()
            try:
                return int(contents)
            except ValueError:
                return 0
    
        else:
            return 0


    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
  
